import json
import pandas as pd
from datetime import timedelta


def iso8601_to_seconds(time: str) -> float:
    """Function converting iso8601 format to python timedelta


    Args:
        time (str): time string in iso8601 format

    Returns:
        timedelta: converted time
    """
    print(time)
    time = time.strip("PT")
    print(time)
    if "D" in time:
        days = time.split("D")[0]
        days = int(days)
        print(days)
        if "DT" in time:
            time = time.split("DT")[1]
    else:
        days = 0
    if "H" in time:
        hours = time.split("H")[0]
        hours = int(hours)
        time = time.split("H")[1]
    else:
        hours = 0
    if "M" in time:
        minutes = time.split("M")[0]
        minutes = int(minutes)
        time = time.split("M")[1]
    else:
        minutes = 0
    if "S" in time:
        seconds = time.split("S")[0]
        seconds = int(seconds)
        time = time.split("S")[1]
    else:
        seconds = 0
    duration = timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()
    return duration


def extract_any(key: json, extracted_field: str) -> object:
    """Function extracting any nested data from json field

    Args:
        column (json): JSON object
        extracted_field (str): key of extracted field

    Returns:
        _type_: _description_
    """

    return key.get(extracted_field)


def extract_channel_id(subtitles: str) -> str or None:
    """Function to extract nested channelId from subtitles field.

    Args:
        subtitles (str): Subtitles filed in DataFrame

    Returns:
        str or None: if subtitles filed is a list function returns channelId, else - None.
    """
    if isinstance(subtitles, list):
        url = subtitles[0].get("url", None)
        if url:
            return url.split("channel/")[1]
    else:
        return None


def extract_video_id(titleUrl: str) -> str or None:
    """Function to extract videoID from titleUrl string.

    Args:
        titleUrl (str): titleUrl filed in DataFrame

    Returns:
        str or None: if titleUrl filed is a string function returns videoId, else - None.
    """
    if isinstance(titleUrl, str):
        return titleUrl.split("=")[1]
    else:
        return None


def JSON_to_DataFrame(videos_data: json) -> pd.DataFrame or None:
    """Function responsible for converting JSON data about single video to DataFrame

    Args:
        videos_data (json): File consisting of history of watched videos

    Returns:
        pd.DataFrame or None: If history file is empty function will return None, else - converted data in DatFrame
    """

    # Dictionary with nested fields as keys and their parents as values.
    columns = {
        "title": "snippet",
        "publishedAt": "snippet",
        "channelId": "snippet",
        "categoryId": "snippet",
        "duration": "contentDetails",
        "viewCount": "statistics",
        "likeCount": "statistics",
        "thumbnails": "snippet",
    }

    if videos_data != []:
        videos_pd = pd.DataFrame(
            videos_data,
            columns=["id", "snippet", "contentDetails", "statistics", "thumbnails"],
        )
    else:
        return None
    # Extracting nested values.
    for key in columns.keys():
        videos_pd[key] = videos_pd[columns[key]].apply(lambda x: extract_any(x, key))
    # extracting double nested fields with thumbnails

    videos_pd["thumbnail"] = [
        extract_any(x, "url")
        for x in [extract_any(x, "high") for x in videos_pd["thumbnails"]]
    ]

    videos_pd = videos_pd.drop(
        columns=["snippet", "contentDetails", "statistics", "thumbnails"]
    )

    videos_pd["publishedAt"] = pd.to_datetime(videos_pd["publishedAt"], format="mixed")

    videos_pd["duration"] = videos_pd["duration"].apply(lambda x: iso8601_to_seconds(x))

    return videos_pd
