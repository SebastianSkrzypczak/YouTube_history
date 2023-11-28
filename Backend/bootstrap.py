"""This is the bootstrapping module that initializes all objects and dependencies.
Function that does that is initialize() and it returns a manger object to further use.
"""

import pandas as pd
from tqdm import tqdm
from icecream import ic
from adapters import file, youtube_api
from domain.model import WatchHistory, Videos, Channels
from service_layer import unit_of_work, data_manipulation
from service_layer.manager import Manager


def create_domain_objects() -> dict:
    """
    Returns:
        dict: object_name: object
    """
    videos = Videos()
    channels = Channels()
    watch_history = WatchHistory(videos)

    return {"videos": videos, "channels": channels, "watch_history": watch_history}


def create_dependencies() -> dict:
    """
    Returns:
        dict: object_name: object
    """
    api = youtube_api.Youtube_API()
    uow = unit_of_work.SqLiteUnitOfWork()

    return {"api": api, "uow": uow}


def load_history(history_file: file.AbstractFile, columns: list[str]) -> dict:
    """_summary_

    Args:
        history_file (file.AbstractFile): An abstraction of file containing of history data from YT.
        columns (list[str]): columns that should be included in result DataFrame

    Returns:
        dict: object_name: object
    """
    json_data = history_file.read()

    history = pd.DataFrame(json_data, columns=columns)

    history["time"] = pd.to_datetime(history["time"], format="ISO8601")

    history["titleUrl"] = history["titleUrl"].apply(
        lambda x: data_manipulation.extract_video_id(x)
    )

    history["url"] = history["subtitles"].apply(
        lambda x: data_manipulation.extract_channel_id(x)
    )

    history = history.drop(columns="subtitles")

    return {"history": history}


def get_videos_details_from_api(
    video_urls: list[str],
    damaged_urls: list[str],
    api: youtube_api.Youtube_API,
    videos: Videos,
    batch_size=50,  # maximum length of urls list for single quotation
) -> None:
    """Function downloading data with YT API and converting it into DataFrame

    Args:
        video_urls (list[str]): list of url to be sent to YT API
    """

    damaged = damaged_urls.to_dict(orient="list")["id"]

    number_of_batches = len(video_urls) // batch_size + 1

    progess_bar = tqdm(
        total=number_of_batches, desc="Downloading Videos Details", unit="item"
    )

    for i in range(batch_size, len(video_urls), batch_size):
        urls_list = list(
            url for url in video_urls[i - batch_size : i] if url not in damaged
        )
        if urls_list:
            videos_data = api.get_videos_info(urls_list)
        else:
            videos_data = []
        if videos_data == []:
            damaged_urls = pd.concat(
                [damaged_urls, pd.DataFrame(urls_list, columns=["id"])],
                ignore_index=True,
            ).drop_duplicates()
        else:
            videos_converted = data_manipulation.JSON_to_DataFrame(videos_data)
            videos.add(videos_converted)
            progess_bar.update(1)


def load_videos_from_db_or_api(
    uow: unit_of_work.AbstractUnitOfWork,
    watch_history: WatchHistory,
    videos: Videos,
    api: youtube_api.Youtube_API,
) -> None:
    """
    Args:
        uow (unit_of_work.AbstractUnitOfWork): object allowing DB interactions
        watch_history (WatchHistory):
        videos (Videos):
        api (youtube_api.Youtube_API):

    Raises:
        e: Reraising any Exceptions during DB operations
    """
    damaged_urls = pd.DataFrame(columns=["id"])

    with uow:
        if uow.damaged_urls is not None:
            damaged_urls = uow.damaged_urls
        try:
            video_urls = list(set(filter(None, watch_history.history["titleUrl"])))
            if uow.inspector.has_table("videos"):
                videos.add(uow.videos)
                ic(len(video_urls))
                new_urls = list(set(video_urls) - set(videos.content["id"]))
                ic(len(new_urls))
                if new_urls:
                    get_videos_details_from_api(new_urls, damaged_urls, api, videos)
            else:
                get_videos_details_from_api(video_urls, damaged_urls, api, videos)
        except Exception as e:
            raise e
        uow.commit("videos", videos.content)
        ic(damaged_urls)
        uow.commit("damaged_urls", damaged_urls)


def initialize() -> Manager:
    """Function creating Manager object for further use.

    Returns:
        Manager: object allowing to interact with data.
    """
    domain_objects = create_domain_objects()
    dependencies = create_dependencies()

    file_path = r"files\history.json"

    domain_objects["watch_history"].history = load_history(
        history_file=file.JSONFIle(file_path),
        columns=domain_objects["watch_history"].columns,
    )["history"]
    load_videos_from_db_or_api(
        uow=dependencies["uow"],
        watch_history=domain_objects["watch_history"],
        videos=domain_objects["videos"],
        api=dependencies["api"],
    )
    manager = Manager(
        history=domain_objects["watch_history"],
        videos=domain_objects["videos"],
    )

    return manager
