"""This module provides functions for processing and transforming data related to YouTube video information.

Functions:
    - iso8601_to_seconds: Convert ISO8601 duration format to Python timedelta.
    - extract_any: Extract any nested data from a JSON field.
    - extract_channel_id: Extract the nested channelId from the subtitles field.
    - extract_video_id: Extract the videoId from the title_url string.
    - JSON_to_DataFrame: Convert JSON data about a single video to a Pandas DataFrame."""

import json
import re
from datetime import timedelta
import pandas as pd


def iso8601_to_seconds(time: str) -> timedelta:
    """Function converting iso8601 format to python timedelta


    Args:
        time (str): time string in iso8601 format

    Returns:
        timedelta: converted time
    """

    if not time:
        raise ValueError

    pattern = r"P(?:(?P<days>\d+)D)?T?(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?"

    match = re.match(pattern, time)

    if not match:
        raise ValueError
    else:
        days = int(match.group("days")) if match.group("days") else 0
        hours = int(match.group("hours")) if match.group("hours") else 0
        minutes = int(match.group("minutes")) if match.group("minutes") else 0
        seconds = int(match.group("seconds")) if match.group("seconds") else 0

    duration = timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()

    return duration


def extract_any(dict: json, extracted_field: str) -> object:
    """Function extracting any nested data from json field

    Args:
        column (json): JSON object
        extracted_field (str): key of extracted field

    Returns:
        _type_: _description_
    """
    return dict.get(extracted_field)


def extract_channel_id(subtitles: str) -> str | None:
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


def extract_video_id(title_url: str) -> str or None:
    """Function to extract videoID from title_url string.

    Args:
        title_url (str): title_url filed in DataFrame

    Returns:
        str or None: if title_url filed is a string function returns videoId, else - None.
    """
    if isinstance(title_url, str):
        return title_url.split("=")[1]
    return None


def JSON_to_DataFrame(videos_data: json) -> pd.DataFrame or None:
    """Function responsible for converting JSON data about single video to DataFrame

    Args:
        videos_data (json): File consisting of history of watched videos

    Returns:
        pd.DataFrame or None: If data is empty function will return None, else - converted data in DatFrame
    """

    # Dictionary with nested fields as keys and their parents as values.
    data = {
        "id": "id",
        "title": "snippet.title",
        "publishedAt": "snippet.publishedAt",
        "channelId": "snippet.channelId",
        "categoryId": "snippet.categoryId",
        "duration": "contentDetails.duration",
        "viewCount": "statistics.viewCount",
        "likeCount": "statistics.likeCount",
        "thumbnail": "snippet.thumbnails.standard.url",
    }

    if videos_data:
        normalized_pd = pd.json_normalize(videos_data)
    else:
        return None
    videos_pd = pd.DataFrame(
        columns=[
            "id",
            "title",
            "publishedAt",
            "channelId",
            "categoryId",
            "duration",
            "viewCount",
            "likeCount",
            "thumbnail",
        ]
    )
    for key in data:
        videos_pd[key] = normalized_pd[data[key]]

    videos_pd["publishedAt"] = pd.to_datetime(videos_pd["publishedAt"], format="mixed")

    videos_pd["duration"] = videos_pd["duration"].apply(lambda x: iso8601_to_seconds(x))

    return videos_pd
