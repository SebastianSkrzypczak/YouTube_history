from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
# from typing import TypeVar, Generic
import json
import logging
import api
import pandas as pd


@dataclass
class Video:
    '''Dataclass to store info about single video'''

    videoId: str = None
    title: str = None
    publishedAt: str = None
    channelId: str = None
    categoryId: int = None
    duration: str = None
    viewCount: int = None
    likeCount: int = None
    # thumbnail

    def add(self, video_data: json):
        if video_data is not []:

            self.videoId = video_data.get('id')

            snippet = video_data.get('snippet')
            self.title = snippet.get('title')
            self.publishedAt = snippet.get('publishedAt')
            self.channelId = snippet.get('channelId')
            self.categoryId = snippet.get('categoryId')

            contentDetails = video_data.get('contentDetails')
            self.duration = contentDetails.get('duration')

            statistics = video_data.get('statistics')
            self.viewCount = statistics.get('viewCount')
            self.likeCount = statistics.get('likeCount')

    def __repr__(self):
        return (f'{self.title}')


@dataclass
class Channel:
    '''Dataclass to store info about single channel'''

    channelId: str = None
    title: str = None
    publishedAt: datetime = None
    viewCount: int = None
    subscriberCount: int = None
    videoCount: int = None
    # banner

    def add(self, channel_data: json):
        if channel_data is not []:

            self.channelId = channel_data.get('id')

            snippet = channel_data.get('snippet')
            self.title = snippet.get('title')
            self.publishedAt = snippet.get('publishedAt')

            statistics = channel_data.get('statistics')
            self.viewCount = statistics.get('viewCont')
            self.subscriberCount = statistics.get('subscriberCount')
            self.videoCount = statistics.get('videoCount')

    def __repr__(self) -> str:
        return self.title


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
        self.urls: list[str] = []
        self.times: list[str] = []
        self.channelsIds: list[str] = []
        self.videos: dict[datetime: Video] = {}
        self.channels: dict[str: Channel] = {}
        self.dataStorage = dataStorage

    def load(self):

        json_data = self.dataStorage.read()
        index = 0
        for record in json_data:
            url = record.get('titleUrl', '=').split('=')[1]
            if url == '':
                continue
                #TODO: deleted videos
            self.urls.append(url)
            time = record.get('time', '')
            self.times.append(time)
            channelId = record.get('subtitles')[0].get('url', 'channel/').split('channel/')[1]
            self.channelsIds.append(channelId)
            index += 1
            if index >= 10:
                break

    def add(self) -> None:

        self.load()
        videos_data = api.get_videos_info(self.urls)
        for element in videos_data:
            video = Video()
            video.add(element)
            self.videos[video.videoId] = video
        channels_data = api.get_channels_info(self.channelsIds)
        for element in channels_data:
            channel = Channel()
            channel.add(element)
            self.channels[channel.channelId] = channel

    def __iter__(self):
        return iter(self.videos)

    def __str__(self):
        str = ''
        for key in self.videos.keys():
            str += f'\n{self.videos[key]}\n'
        return str



def main():
    dataStorage = DataStorage('history.json')
    history = WatchHistory(dataStorage=dataStorage)
    history.add()
    history = pd.read_json('history.json')
    print(history)


if __name__ == "__main__":
    main()

#TODO: write down all desired features
#TODO: 