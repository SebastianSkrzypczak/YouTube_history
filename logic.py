import data
from datetime import timedelta
import pandas as pd


def calculate_total_watch_time(history: data.WatchHistory, videos: data.Videos):
    merged = history.watch_history.merge(videos.content, left_on='titleUrl', right_on='id', how='inner')
    return timedelta(seconds=merged['duration'].sum())


def show_most_viewed_videos(history: data.WatchHistory, videos: data.Videos, count: int):
    most_viewed_ids = history.watch_history['titleUrl'].value_counts().sort_values(ascending=False).head(10)
    pandas_most_viewed = pd.DataFrame(zip(most_viewed_ids.index.to_list(), most_viewed_ids.values.tolist()), columns=['id', 'count'])
    merged = pandas_most_viewed.merge(videos.content, how='inner')
    merged = merged.drop(columns=['publishedAt', 'channelId', 'categoryId', 'duration', 'viewCount', 'likeCount'])
    return merged


def show_most_viewed_channels(history: data.WatchHistory):
    most_viewed_id = history.watch_history['titleUrl'].value_counts().idxmax()
    view_count = history.watch_history['titleUrl'].value_counts().max()
    return most_viewed_id, view_count


def time_activity_analysis(history: data.WatchHistory):
    '''On what time You watch the most movies'''
    watch_history = history.watch_history.copy()
    watch_history['hours'] = watch_history['time'].dt.hour
    hourly_count = dict(watch_history['hours'].value_counts().sort_index())
    return hourly_count


def category_analysis():
    '''Which cattegories are watched the most + in time + %'''
    pass


def average_video_duration(videos: data.Videos):
    return timedelta(seconds=videos.content['duration'].mean())


def key_words_title():
    pass


def statistics_in_time():
    pass


def average_break():
    pass
