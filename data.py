from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
# from typing import TypeVar, Generic
import json
import logging
import api
import pandas as pd


def extract_any(column: json, extracted_field: str):
    return column.get(extracted_field)


def iso8601_to_timedelta(time: str):
    time = time.strip('PT')
    if 'H' in time:
        hours = time.split('H')[0]
        hours = int(hours)
        time = time.split('H')[1]
    else:
        hours = 0
    if 'M' in time:
        minutes = time.split('M')[0]
        minutes = int(minutes)
        time = time.split('M')[1]
    else:
        minutes = 0
    seconds = time.split('S')[0]
    if seconds != '':
        seconds = int(seconds)
    else:
        seconds = 0
    duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return duration


class Videos:
    '''Dataclass to store info about single video'''
    def __init__(self,) -> None:
        self.content = pd.DataFrame(columns=[
                                            'id',
                                            'title',
                                            'publishedAt',
                                            'channelId',
                                            'categoryId',
                                            'duration',
                                            'viewCount',
                                            'likeCount'
                                            ])
        self.columns = {
                        'title': 'snippet',
                        'publishedAt': 'snippet',
                        'channelId': 'snippet',
                        'categoryId': 'snippet',
                        'duration': 'contentDetails',
                        'viewCount': 'statistics',
                        'likeCount': 'statistics'
                       }

    def add(self, videos_data: json):
        if videos_data is not []:
            videos_pd = pd.DataFrame(videos_data, columns=['id', 'snippet', 'contentDetails', 'statistics'])
        else:
            return None
        for key in self.columns.keys():
            videos_pd[key] = videos_pd[self.columns[key]].apply(lambda x: extract_any(x, key))

        videos_pd = videos_pd.drop(columns=['snippet', 'contentDetails', 'statistics'])
        videos_pd['publishedAt'] = pd.to_datetime(videos_pd['publishedAt'], format = 'mixed')
        videos_pd['duration'] = videos_pd['duration'].apply(lambda x: iso8601_to_timedelta(x))
        self.content = pd.concat([self.content, videos_pd], axis=0, ignore_index=True)


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

    def __init__(self) -> None:
        self.dataStorage = DataStorage('history.json')
        self.watch_history = None
        self.columns = [
            'titleUrl',
            'time',
            'subtitles'
        ]
        self.videos = None

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
        video_urls = list(filter(None, self.watch_history['titleUrl']))
        channel_urls = list(filter(None, self.watch_history['url']))
        videos_data = api.get_videos_info(video_urls[0:50])
        channels_data = api.get_channels_info(channel_urls[0:50])
        self.videos = Videos()
        self.videos.add(videos_data)


def main():
    ...


if __name__ == "__main__":
    main()

# TODO: write down all desired features
# TODO: DOCSTRINGS
# TODO: Exceptions and ErrorsHandlig
# TODO: MAX 50 urls
# TODO: channels
