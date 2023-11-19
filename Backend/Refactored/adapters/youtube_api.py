from googleapiclient.discovery import build
import json


class Youtube_API:
    def __init__(self) -> None:
        self.youtube = self.set_up()

    def set_up(self) -> object:
        try:
            api_file = open('API.txt', 'r')
        except FileNotFoundError as e:
            raise e
        API_KEY = api_file.readline()
        try:
            return build('youtube', 'v3', developerKey=API_KEY)
        except Exception as e:
            raise e

    def get_videos_info(self, video_ids) -> json:
        response = self.youtube.videos().list(part='snippet,contentDetails,statistics',
                                              id=','.join(video_ids)).execute()
        if response.get('items'):
            formatted_json = response.get('items')
            return formatted_json
        else:
            return []

    def get_channels_info(self, channels_ids,) -> json:

        response = self.youtube.channels().list(part='snippet,statistics,brandingSettings,contentDetails',
                                                id=','.join(channels_ids)).execute()
        if response.get('items'):
            formatted_json = response.get('items')
            return formatted_json
        else:
            return []
