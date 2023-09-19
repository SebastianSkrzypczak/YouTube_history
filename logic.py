import data
from datetime import timedelta, datetime
import pandas as pd
from icecream import ic 


def filter_videos_by(column_name: str, videos: pd.DataFrame, categories: list, exclude: bool) -> pd.DataFrame:
    if exclude is True:
        videos_filtered = videos[~videos[column_name].isin(categories)]
    else:
        videos_filtered = videos[videos[column_name].isin(categories)]
    return videos_filtered


def filter_videos_by_date(column_name: str, start_date: datetime, end_date: datetime, videos: pd.DataFrame, exclude = False):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(start_date)
    if exclude is False:
        ic(videos[column_name])
        videos_filtered = videos[end_date > videos[column_name] > start_date]
    else:
        videos_filtered = videos[start_date > videos[column_name] or end_date < videos[column_name]]
    return videos_filtered



def any_analysis(analysis_by: str, history: pd.DataFrame, videos: pd.DataFrame,
                 column_name = '', categories=[], exclude=True,
                 columns_to_add: list[str] = '',
                 count=10):
    '''Which cattegories are watched the most + in time + %'''
    if column_name != '':
        videos = filter_videos_by(column_name, videos, categories, exclude=exclude)
    merged = history.merge(videos, how='inner', left_on='titleUrl', right_on='id')
    columns_to_drop = list(set(merged.columns.to_list()) - set([analysis_by]))
    merged = merged.drop(columns=columns_to_drop)
    merged = merged[analysis_by].value_counts().sort_values(ascending=False).head(count)
    merged_pd = pd.DataFrame(zip(list(merged.index), list(merged.values)), columns=[analysis_by, 'count'])
    return merged_pd


def calculate_total_watch_time(history: pd.DataFrame, videos: pd.DataFrame, column_name: str = "", categories: list = [], exclude: bool = True ):
    merged = history.merge(videos, left_on='titleUrl', right_on='id', how='inner')
    if column_name != "":
        merged = filter_videos_by(column_name, videos, categories, exclude)
    return timedelta(seconds=merged['duration'].sum())


def show_most_viewed_videos(history: pd.DataFrame, videos: pd.DataFrame, count: int, excluded_categories: list = [], channels: list = []) -> pd.DataFrame:
    most_viewed_DF = any_analysis('id', history, videos, column_name='categoryId', categories=excluded_categories, count=count)
    merged = most_viewed_DF.merge(videos, how='inner')
    merged = merged.drop(columns=['publishedAt', 'channelId', 'categoryId', 'duration', 'viewCount', 'likeCount'])
    return merged


def show_most_viewed_channels(history: pd.DataFrame, videos: pd.DataFrame, excluded_categories: list[str] = []):
    filtered_videos = filter_videos_by('categoryId', videos, excluded_categories, exclude=True)
    print(filtered_videos)
    most_viewed_id = history['titleUrl'].value_counts().idxmax()
    view_count = history['titleUrl'].value_counts().max()
    return most_viewed_id, view_count


def time_activity_analysis(history: pd.DataFrame):
    '''On what time You watch the most movies'''
    watch_history = history.copy()
    watch_history['hours'] = watch_history['time'].dt.hour
    hourly_count = dict(watch_history['hours'].value_counts().sort_index())
    return hourly_count


def average_video_duration(videos: data.Videos):
    return timedelta(seconds=videos.content['duration'].mean())


def key_words_title():
    pass


def statistics_in_time(history: pd.DataFrame, videos: pd.DataFrame, ):
    watch_history = history.copy()
    years = set(watch_history['time'].dt.year)
    merged = history.merge(videos, left_on='titleUrl', right_on='id')
    for year in years:
        filtered_by_year = filter_videos_by_date(column_name='time', start_date=pd.to_datetime(str(year)),
                                                 end_date=pd.to_datetime(str(year))-timedelta(days=1), videos=merged)
        ic(filtered_by_year)
    return watch_history



def average_break():
    pass
