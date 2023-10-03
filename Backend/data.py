from abc import ABC, abstractmethod
from datetime import timedelta
from sqlalchemy import create_engine, inspect
from tqdm import tqdm
import json
import logging
import api
import pandas as pd
from icecream import ic


engine = create_engine('sqlite:///history.db')
inspector = inspect(engine)


def extract_any(column: json, extracted_field: str):
    '''Function extracting any column from json data'''

    return column.get(extracted_field)


def iso8601_to_timedelta(time: str):
    '''Function converting iso8601 format to python timedelta'''

    time = time.strip('PT')
    if 'DT' in time:
        days = time.split('DT')[0]
        days = int(days)
        time = time.split('DT')[1]
    else:
        days = 0
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
    if 'S' in time:
        seconds = time.split('S')[0]
        seconds = int(seconds)
        time = time.split('S')[1]
    else:
        seconds = 0
    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds).total_seconds()
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
                                            # 'thumbnails'
                                            ])

    def add(self, videos_data: pd.DataFrame):
        if videos_data is not []:
            self.content = pd.concat([self.content, videos_data], axis=0, ignore_index=True)


class Channels:
    '''Dataclass to store info about single channel'''

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
              # 'thumbnails',

              ]

    def add(self, channels_data: json):
        if channels_data is not []:
            self.channels = pd.DataFrame(channels_data, columns=self.columns)


class Repository(ABC):

    @abstractmethod
    def add(self) -> None:
        pass


class DataStorage(ABC):

    @abstractmethod
    def read():
        ...


class JSONFIle(DataStorage):
    '''Class to handle JSON files'''

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


class SQLFile(DataStorage):
    '''Class to handle SQL manipulation'''

    def __init__(self) -> None:
        pass

    def read(self, table_name):
        df = pd.read_sql_table(table_name, engine)
        return df

    def write(self, table_name, data: pd.DataFrame):
        data['duration']
        data.to_sql(table_name, engine, if_exists='replace', index=False)


class WatchHistory(Repository):

    def __init__(self) -> None:
        self.dataStorage = JSONFIle('history.json')
        self.watch_history = None
        self.columns = [
            'titleUrl',
            'time',
            'subtitles'
        ]
        self.videos = None
        self.sql = SQLFile()

    def extract_channel_id(self, subtitles) -> str or None:
        if isinstance(subtitles, list):
            url = subtitles[0].get('url', None)
            if url:
                return url.split('channel/')[1]
        else:
            return None

    def extract_video_id(self, titleUrl: str) -> str or None:
        if isinstance(titleUrl, str):
            return titleUrl.split('=')[1]
        else:
            return None

    def JSON_to_DataFrame(self, videos_data: json) -> pd.DataFrame or None:
        columns = {
                'title': 'snippet',
                'publishedAt': 'snippet',
                'channelId': 'snippet',
                'categoryId': 'snippet',
                'duration': 'contentDetails',
                'viewCount': 'statistics',
                'likeCount': 'statistics'
                }
        if videos_data != []:
            videos_pd = pd.DataFrame(videos_data, columns=['id', 'snippet', 'contentDetails', 'statistics'])
        else:
            return None
        for key in columns.keys():
            videos_pd[key] = videos_pd[columns[key]].apply(lambda x: extract_any(x, key))
        videos_pd = videos_pd.drop(columns=['snippet', 'contentDetails', 'statistics'])
        videos_pd['publishedAt'] = pd.to_datetime(videos_pd['publishedAt'], format = 'mixed')
        videos_pd['duration'] = videos_pd['duration'].apply(lambda x: iso8601_to_timedelta(x))
        return videos_pd

    def load(self) -> None:
        json_data = self.dataStorage.read()
        self.watch_history = pd.DataFrame(json_data, columns=self.columns)
        self.watch_history['time'] = pd.to_datetime(self.watch_history['time'], format='ISO8601')
        self.watch_history['titleUrl'] = self.watch_history['titleUrl'].apply(lambda x: self.extract_video_id(x))
        self.watch_history['url'] = self.watch_history['subtitles'].apply(lambda x: self.extract_channel_id(x))
        self.watch_history = self.watch_history.drop(columns='subtitles')

    def get_api(self, video_urls) -> None:
        batch_size = 50
        number_of_bathces = len(video_urls) // batch_size + 1
        progess_bar = tqdm(total=number_of_bathces, desc='Downloading Videos Details', unit='item')
        for i in range(batch_size, len(video_urls), batch_size):
            videos_data = api.get_videos_info(video_urls[i-batch_size:i])
            videos_converted = self.JSON_to_DataFrame(videos_data)
            self.videos.add(videos_converted)
            progess_bar.update(1)

    def add(self) -> None:
        self.load()
        self.videos = Videos()
        video_urls = list(set(filter(None, self.watch_history['titleUrl'])))
        if inspector.has_table('videos'):
            videos_data = self.sql.read('videos')
            self.videos.add(videos_data)
            new_urls = list(set(video_urls) - set(self.videos.content['id']))
            if new_urls is not []:
                pass
                # self.get_api(new_urls)
        else:
            self.get_api(video_urls)
        # channel_urls = list(filter(None, self.watch_history['url']))
        # channels_data = api.get_channels_info(channel_urls[0:50])

    def save(self) -> None:
        self.sql.write('videos', self.videos.content)


def main():
    ...


if __name__ == "__main__":
    main()

# TODO: write down all desired features
# TODO: DOCSTRINGS
# TODO: Exceptions and ErrorsHandlig
# TODO: MAX 50 urls
# TODO: channels
# TODO: SQL
# TODO: shorts
