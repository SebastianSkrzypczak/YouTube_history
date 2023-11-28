"""This module provides a class for interacting with the YouTube Data API to retrieve information
about videos and channels."""

import json
import logging
from googleapiclient.discovery import build, Resource


FILE_PATH = r"API.txt"

logger = logging.getLogger(__name__)


class Youtube_API:
    def __init__(self, file_path: str = FILE_PATH) -> None:
        self.file_path = file_path
        self.youtube = self.set_up()

    def set_up(self) -> Resource:
        try:
            with open(self.file_path, "r") as file:
                API_KEY = file.readline()
        except FileNotFoundError as e:
            raise e
        try:
            return build("youtube", "v3", developerKey=API_KEY)
        except Exception as e:
            logger.error(e)
            raise e

    def get_videos_info(self, video_ids) -> json:
        response = (
            self.youtube.videos()
            .list(part="snippet,contentDetails,statistics", id=",".join(video_ids))
            .execute()
        )
        if response.get("items"):
            formatted_json = response.get("items")
            return formatted_json
        else:
            return []

    def get_channels_info(
        self,
        channels_ids,
    ) -> json:
        response = (
            self.youtube.channels()
            .list(
                part="snippet,statistics,brandingSettings,contentDetails",
                id=",".join(channels_ids),
            )
            .execute()
        )
        if response.get("items"):
            formatted_json = response.get("items")
            return formatted_json
        return []
