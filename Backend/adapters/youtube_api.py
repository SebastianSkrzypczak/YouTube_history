from googleapiclient.discovery import build, Resource
import json
import logging
from os.path import abspath

FILE_PATH = abspath(r"API.txt")


class Youtube_API:
    def __init__(self, file_path=FILE_PATH) -> None:
        self.file_path = file_path
        self.youtube = self.set_up()

    def set_up(self) -> Resource:
        try:
            api_file = open(self.file_path, "r")
        except FileNotFoundError as e:
            raise e
        API_KEY = api_file.readline()
        try:
            return build("youtube", "v3", developerKey=API_KEY)
        except Exception as e:
            logging.error(e)
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
        else:
            return []
