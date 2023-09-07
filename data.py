from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
# from typing import TypeVar, Generic
import json
import logging
import services


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
            self.title = video_data.get('title')

            snippet = video_data.get('snippet')
            self.publishedAt = snippet.get('publishedAt')
            self.channelId = snippet.get('channelId')
            self.categoryId = snippet.get('categoryId')

            contentDetails = video_data.get('contentDetails')
            self.duration = contentDetails.get('duration')

            statistics = video_data.get('statistics')
            self.viewCount = statistics.get('viewCount')
            self.likeCount = statistics.get('likeCount')

    def __str__(self):
        return (f'{self.videoId}\n{self.publishedAt}\n{self.channelId}')    


@dataclass
class Channel:
    '''Dataclass to store info about single channel'''

    channelId: str
    title: str
    publishedAt: datetime
    viewCount: int
    subscriberCount: int
    videoCount: int
    # banner


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
        self.videos: dict[datetime: Video] = {}
        self.dataStorage = dataStorage

    def load_urls_and_times(self):
        json_data = self.dataStorage.read()
        index = 0
        for record in json_data:
            url = record.get('titleUrl', '').split('=')[1]
            if url == '':
                break
            self.urls.append(url)
            time = record.get('time', '')
            self.times.append(time)
            index += 1
            if index >= 10:
                break

    def add(self) -> None:

        self.load_urls_and_times()
        data = services.get_videos_info(self.urls)
        index = 0
        for element in data:
            video = Video()
            video.add(element)
            self.videos[self.times[index]] = video
            index += 1

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
    print(history)


if __name__ == "__main__":
    main()

#TODO: write down all desired features
#TODO: 