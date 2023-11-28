import json
import logging
import pandas as pd


class Videos:
    """Class to store videos data"""

    def __init__(
        self,
    ) -> None:
        self.content: pd.DataFrame = pd.DataFrame(
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

    def add(self, videos_data: pd.DataFrame):
        if not videos_data.empty:
            self.content = pd.concat(
                [self.content, videos_data], axis=0, ignore_index=True
            )
        else:
            logging.debug("empty videos data")


class Channels:
    """Class to store info about channels"""

    def __init__(self) -> None:
        self.channels = None
        self.columns = [
            "id",
            "title",
            "publishedAt",
            "country",
            "viewCount",
            "subscriberCount",
            "videoCount",
            "keywords",
            "thumbnail",
        ]

    def add(self, channels_data: json):
        if channels_data:
            self.channels = pd.DataFrame(channels_data, columns=self.columns)


class WatchHistory:
    """Class to store and manipulte data about history for watched videos"""

    def __init__(self, videos: Videos) -> None:
        self.videos = videos
        self.columns = ["titleUrl", "time", "subtitles"]
        self.history: pd.DataFrame = None
        self.damaged_urls: list[str] = []

        # self.sql = SQLFile()
        # self.youtube = api.set_up()

        # if inspector.has_table('damaged_urls'):
        #     self.damaged_urls = self.sql.read('damaged_urls')
        # else:
        #     self.damaged_urls = pd.DataFrame(columns=['id'])
