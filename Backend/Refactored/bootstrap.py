from adapters import file, youtube_api
from domain.model import WatchHistory, Videos, Channels
from service_layer import unit_of_work, data_manipulation, logic
import pandas as pd
from tqdm import tqdm
from icecream import ic


class Bootstrap:
    def __init__(
        self,
        history_file: file.AbstractFile = file.JSONFIle(
            r'Backend\Refactored\files\history.json'),
    ) -> None:
        self.history_file = history_file
        self.api = None
        self.uow = None
        self.watch_history = None
        self.videos = None
        self.channels = None
        self.damaged_urls = pd.DataFrame(columns=['id'])

    def create_domain_objects(self) -> None:
        self.videos = Videos()
        self.channels = Channels()
        self.watch_history = WatchHistory(self.videos)

    def create_dependencies(self) -> None:
        self.api = youtube_api.Youtube_API()
        self.uow = unit_of_work.SqLiteUnitOfWork()

    def load_history(self) -> None:
        """Function loading data about history items from JSON and converting it to DataFrame with whole history
        """
        json_data = self.history_file.read()

        history = pd.DataFrame(json_data, columns=self.watch_history.columns)

        history['time'] = pd.to_datetime(
            history['time'], format='ISO8601')

        history['titleUrl'] = history['titleUrl'].apply(
            lambda x: data_manipulation.extract_video_id(x))

        history['url'] = history['subtitles'].apply(
            lambda x: data_manipulation.extract_channel_id(x))

        self.watch_history.history = history.drop(columns='subtitles')

    def load_videos_from_DB_or_API(self) -> None:
        """Function to
        """
        with self.uow:
            if self.uow.damaged_urls is not None:
                self.damaged_urls = self.uow.damaged_urls
                ic(self.damaged_urls)
            try:
                video_urls = list(
                    set(filter(None, self.watch_history.history['titleUrl'])))
                if self.uow.inspector.has_table('videos'):
                    self.videos.add(self.uow.videos)
                    ic(len(video_urls))
                    new_urls = list(set(video_urls) -
                                    set(self.videos.content['id']))
                    ic(len(new_urls))
                    if new_urls is not []:
                        self.get_videos_details_from_api(new_urls)
                else:
                    self.get_videos_details_from_api(video_urls)
            except Exception as e:
                raise e
            self.uow.commit('videos', self.videos.content)
            ic(self.damaged_urls)
            self.uow.commit('damaged_urls', self.damaged_urls)

    def get_videos_details_from_api(
            self,
            video_urls: list[str],
            batch_size=50,
    ) -> None:
        """Function downloading data with YT API and converting it into DataFrame

        Args:
            video_urls (list[str]): list of url to be sent to YT API
        """

        damaged = self.damaged_urls.to_dict(orient='list')['id']
        # maximum length of urls list for single quotation
        number_of_batches = len(video_urls) // batch_size + 1
        progess_bar = tqdm(total=number_of_batches,
                           desc='Downloading Videos Details', unit='item')
        for i in range(batch_size, len(video_urls), batch_size):
            urls_list = list(
                url for url in video_urls[i-batch_size:i] if url not in damaged)
            if urls_list != []:
                videos_data = self.api.get_videos_info(urls_list)
            else:
                videos_data = []
            if videos_data == []:
                self.damaged_urls = pd.concat([self.damaged_urls, pd.DataFrame(
                    urls_list, columns=['id'])], ignore_index=True).drop_duplicates()
            else:
                videos_converted = data_manipulation.JSON_to_DataFrame(
                    videos_data)
                self.videos.add(videos_converted)
                progess_bar.update(1)


def initialize() -> Bootstrap:
    bootstrap = Bootstrap()
    bootstrap.create_domain_objects()
    bootstrap.create_dependencies()
    bootstrap.load_history()
    bootstrap.load_videos_from_DB_or_API()
    return bootstrap


def main():
    data = initialize()
    ic(logic.average_video_duration(data.videos))


if __name__ == '__main__':
    main()
