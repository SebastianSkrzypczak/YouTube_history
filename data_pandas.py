from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
# from typing import TypeVar, Generic
import json
import logging
import api
import pandas as pd


class Videos:
    '''Dataclass to store info about single video'''
    def __init__(self) -> None:
        self.videos = None
        self.columns = [
              'videoId',
              'title',
              'publishedAt',
              'channelId',
              'categoryId',
              'duration',
              'viewCount',
              'likeCount'
              ]

    def add(self, videos_data: json):
        if videos_data is not []:
            self.videos = pd.DataFrame(columns=self.columns)
            for video_data in videos_data:
                row = {
                    'videoId': video_data['videoId'],
                    'title': video_data['snippet']['title'],
                    'publishedAt': video_data['snippet']['publishedAt'],
                    'channelId': video_data['snippet']['channelId'],
                    'categoryId': video_data['snippet']['categoryId'],
                    'duration': video_data['contentDetails']['duration'],
                    'viewCount': video_data['contentDetails']['viewCount'],
                    'likeCount': video_data['contentDetails']['likeCount']
                }
            self.videos = self.videos.append(row, ignoreIndex=True)


class Channels:
    '''Dataclass to store info about single channel'''
    def __init__(self) -> None:
        self.channels = None
        self.columns = [
              'channelId',
              'title',
              'publishedAt',
              'viewCount',
              'subscriberCount',
              'videoCount',
              # 'banner'
              ]

    def add(self, channels_data: json):
        if channels_data is not []:
            self.channels = pd.DataFrame(channels_data, columns=self.columns)


class Repository(ABC):

    @abstractmethod
    def add(self) -> None:
        pass


class DataStorage:

    def __init__(self, file) -> None:
        self.file = file

    def read(self) -> json:
        with open(self.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        json_lines = ''.join(lines)
        try:
            json_data = json.loads(json_lines)
        except json.JSONDecodeError as e:
            logging.debug(e)
        return json_data


class WatchHistory(Repository):
    def __init__(self, dataStorage: DataStorage) -> None:
        self.dataStorage = dataStorage
        self.watch_history = None
        self.columns = [
            'titleUrl',
            'time',
            'subtitles'
        ]

    def extract_channel_id(self, subtitles):
        if isinstance(subtitles, list):
            url = subtitles[0].get('url', None)
            if url:
                return url.split('channel/')[1]
        else:
            return None

    def extract_video_id(self, titleUrl: str):
        if isinstance(titleUrl, str):
            return titleUrl.split('=')[1]
        else:
            return None

    def load(self):
        json_data = self.dataStorage.read()
        self.watch_history = pd.DataFrame(json_data, columns=self.columns)
        self.watch_history['time'] = pd.to_datetime(self.watch_history['time'], format='ISO8601')
        self.watch_history['titleUrl'] = self.watch_history['titleUrl'].apply(lambda x: self.extract_video_id(x))
        self.watch_history['url'] = self.watch_history['subtitles'].apply(lambda x: self.extract_channel_id(x))
        self.watch_history = self.watch_history.drop(columns='subtitles')

    def add(self) -> None:
        self.load()
        video_urls = list(self.watch_history['titleUrl'])
        channel_urls = list(self.watch_history['url'])
        videos_data = api.get_videos_info(video_urls)
        channels_data = api.get_channels_info(channel_urls)
        for video in videos_data:
            


def main():
    dataStorage = DataStorage('history.json')
    history = WatchHistory(dataStorage=dataStorage)
    history.add()


if __name__ == "__main__":
    main()

#TODO: write down all desired features
#TODO: 