import pandas as pd
import json
import tqdm


class Videos:
    '''Class to store videos data'''

    def __init__(self,) -> None:
        self.content = pd.DataFrame(columns=[
            'id',
            'title',
            'publishedAt',
            'channelId',
            'categoryId',
            'duration',
            'viewCount',
            'likeCount',
            'thumbnail'
        ])

    def add(self, videos_data: pd.DataFrame):
        if videos_data is not []:
            self.content = pd.concat(
                [self.content, videos_data], axis=0, ignore_index=True)


class Channels:
    '''Class to store info about channels'''

    def __init__(self) -> None:
        self.channels = None
        self.columns = [
            'id',
            'title',
            'publishedAt',
            'country',
            'viewCount',
            'subscriberCount',
            'videoCount',
            'keywords',
            'thumbnail',
        ]

    def add(self, channels_data: json):
        if channels_data is not []:
            self.channels = pd.DataFrame(channels_data, columns=self.columns)


class WatchHistory:
    """Class to store and manipulte data about history for watched videos"""

    def __init__(self, history_file: json, videos: Videos) -> None:
        self.history_file = history_file  # JSONFIle('history.json')
        self.videos = videos
        self.columns = [
            'titleUrl',
            'time',
            'subtitles'
        ]
        self.history = None

        # self.sql = SQLFile()
        # self.youtube = api.set_up()

        # if inspector.has_table('damaged_urls'):
        #     self.damaged_urls = self.sql.read('damaged_urls')
        # else:
        #     self.damaged_urls = pd.DataFrame(columns=['id'])

    def extract_channel_id(self, subtitles: str) -> str or None:
        """Function to extract nested channelId from subtitles field.

        Args:
            subtitles (str): Subtitles filed in DataFrame

        Returns:
            str or None: if subtitles filed is a list function returns channelId, else - None. 
        """
        if isinstance(subtitles, list):
            url = subtitles[0].get('url', None)
            if url:
                return url.split('channel/')[1]
        else:
            return None

    def extract_video_id(self, titleUrl: str) -> str or None:
        """Function to extract videoID from titleUrl string.

        Args:
            titleUrl (str): titleUrl filed in DataFrame

        Returns:
            str or None: if titleUrl filed is a string function returns videoId, else - None.
        """
        if isinstance(titleUrl, str):
            return titleUrl.split('=')[1]
        else:
            return None

    def JSON_to_DataFrame(self, videos_data: json) -> pd.DataFrame or None:
        """Function responsible for converting JSON data about single video to DataFrame

        Args:
            videos_data (json): File consisting of history of watched videos

        Returns:
            pd.DataFrame or None: If history file is empty function will return None, else - converted data in DatFrame
        """

        # Dictionary with nested fields as keys and their parents as values.
        columns = {
            'title': 'snippet',
            'publishedAt': 'snippet',
            'channelId': 'snippet',
            'categoryId': 'snippet',
            'duration': 'contentDetails',
            'viewCount': 'statistics',
            'likeCount': 'statistics',
            'thumbnails': 'snippet',
        }

        if videos_data != []:
            videos_pd = pd.DataFrame(videos_data, columns=[
                'id', 'snippet', 'contentDetails', 'statistics', 'thumbnails'])
        else:
            return None
        # Extracting nested values.
        for key in columns.keys():
            videos_pd[key] = videos_pd[columns[key]].apply(
                lambda x: extract_any(x, key))
        # extracting double nested fields with thumbnails

        videos_pd['thumbnail'] = [extract_any(x, 'url') for x in [
            extract_any(x, 'high') for x in videos_pd['thumbnails']]]

        videos_pd = videos_pd.drop(
            columns=['snippet', 'contentDetails', 'statistics', 'thumbnails'])

        videos_pd['publishedAt'] = pd.to_datetime(
            videos_pd['publishedAt'], format='mixed')

        videos_pd['duration'] = videos_pd['duration'].apply(
            lambda x: iso8601_to_timedelta(x))

        return videos_pd

    def load_history(self) -> None:
        """Function loading data about  history items from JSON and converting it to DataFrame with whole history
        """
        json_data = self.history_file

        self.watch_history = pd.DataFrame(json_data, columns=self.columns)

        self.watch_history['time'] = pd.to_datetime(
            self.watch_history['time'], format='ISO8601')

        self.watch_history['titleUrl'] = self.watch_history['titleUrl'].apply(
            lambda x: self.extract_video_id(x))

        self.watch_history['url'] = self.watch_history['subtitles'].apply(
            lambda x: self.extract_channel_id(x))

        self.watch_history = self.watch_history.drop(columns='subtitles')
