import data
from datetime import timedelta, datetime
import pandas as pd
from icecream import ic


def filter_videos_by(column_name: str, videos: pd.DataFrame, categories: list, exclude: bool) -> pd.DataFrame:
    """Function to filter given data in or out of data frame

    Args:
        column_name (str): name of column to be filtered
        videos (pd.DataFrame): dataframe of all videos
        categories (list): list of all exluded or included values
        exclude (bool): exclude or include

    Returns:
        pd.DataFrame: filtered data frame in same format as input
    """

    if exclude is True:
        videos_filtered = videos[~videos[column_name].isin(categories)]
    else:
        videos_filtered = videos[videos[column_name].isin(categories)]
    return videos_filtered


def filter_videos_by_date(column_name: str, start_date: datetime, end_date: datetime, videos: pd.DataFrame, exclude=False) -> pd.DataFrame:
    """Funtion to filter dataframe by date. Date should be in between start and end date.

    Args:
        column_name (str): name of column to be filtered
        start_date (datetime): begin of date interval
        end_date (datetime): end of date interval
        videos (pd.DataFrame): dataframe of all videos
        exclude (bool, optional): defaults to False.

    Returns:
        pd.DataFrame: filtered data frame in same format as input
    """

    start_date = pd.to_datetime(start_date).tz_localize('UTC')
    end_date = pd.to_datetime(end_date).tz_localize('UTC')
    if not exclude:
        videos_filtered = videos[(videos[column_name] >= start_date) & (videos[column_name] <= end_date)]
    else:
        videos_filtered = videos[(videos[column_name] < start_date) | (videos[column_name] > end_date)]
    return videos_filtered


def any_analysis(analysis_by: str, history: pd.DataFrame, videos: pd.DataFrame, name = '',
                 column_name = '', categories=[], exclude=True,
                 columns_to_add: list[str] = '',
                 count=10) -> pd.DataFrame:
    """Function to analise any column in data frame. Function picks top occurences in given column. 

    Args:
        analysis_by (str): columnt to be analise
        history (pd.DataFrame): dataframe with user history
        videos (pd.DataFrame): dataframe with all videos in history
        column_name (str, optional): column name to be filtered. Defaults to ''.
        categories (list, optional):  list of all exluded or included values. Defaults to [].
        exclude (bool, optional): Defaults to True.
        columns_to_add (list[str], optional): Defaults to ''.
        count (int, optional): How many of top occurences should be returned. Defaults to 10.

    Returns:
        pd.DataFrame: dataframe consisting of top occurences
    """

    # Which cattegories are watched the most + in time + %

    if column_name != '':
        videos = filter_videos_by(column_name, videos, categories, exclude=exclude)
    if name == '':
        name = analysis_by
    merged = history.merge(videos, how='inner', left_on='titleUrl', right_on='id')
    columns_to_drop = list(set(merged.columns.to_list()) - set([analysis_by]))
    merged = merged.drop(columns=columns_to_drop)
    merged = merged[analysis_by].value_counts().sort_values(ascending=False).head(count)
    merged_pd = pd.DataFrame(zip(list(merged.index), list(merged.values)), columns=[name, 'count'])
    return merged_pd


def calculate_total_watch_time(history: pd.DataFrame, videos: pd.DataFrame, column_name: str = "", categories: list = [], exclude: bool = True ) -> float:
    """Function to calculate total watch time in whole user history.

    Args:
        history (pd.DataFrame): dataframe with user history
        videos (pd.DataFrame): dataframe with all videos in history
        column_name (str, optional): column name to be filtered. Defaults to ''.
        categories (list, optional):  list of all exluded or included values. Defaults to [].
        exclude (bool, optional): Defaults to True.

    Returns:
        float: total watch time in seconds
    """
    merged = history.merge(videos, left_on='titleUrl', right_on='id', how='inner')
    if column_name != "":
        merged = filter_videos_by(column_name, videos, categories, exclude)
    return merged['duration'].sum()


def show_most_viewed_videos(history: pd.DataFrame, videos: pd.DataFrame, count: int, excluded_categories: list = []) -> pd.DataFrame:
    """Funtion to show most viewed viedeos in user history.

    Args:
        history (pd.DataFrame): dataframe with user history
        videos (pd.DataFrame): dataframe with all videos in history
        count (int): How many of top occurences should be returned.
        excluded_categories (list, optional): vidoes categories to be excluded. Defaults to [].
        channels (list, optional): channels to be excluded. Defaults to [].

    Returns:
        pd.DataFrame: dataframe consisting of most viewed vidoes
    """
    most_viewed_DF = any_analysis('id', history, videos, column_name='categoryId', categories=excluded_categories, count=count)
    merged = most_viewed_DF.merge(videos, how='inner')
    merged = merged.drop(columns=['publishedAt', 'channelId', 'categoryId', 'duration', 'viewCount', 'likeCount'])
    return merged


def show_most_viewed_channels(history: pd.DataFrame, videos: pd.DataFrame, count: int = 10):
    """Funtion to show most viewed channels in user history.

    Args:
        history (pd.DataFrame): dataframe with user history
        videos (pd.DataFrame): dataframe with all videos in history
        count (int): How many of top occurences should be returned.

    Returns:
        _type_: _description_
    """
    most_viewed = any_analysis('channelId', history, videos)
    return most_viewed


def time_activity_analysis(history: pd.DataFrame, start_date = pd.Timestamp.min, end_date = datetime.today()) -> pd.DataFrame:
    """Function to calculate count of videos watched by hours

    Args:
        history (pd.DataFrame): dataframe of user history
        start_date (_type_, optional): begin of date interval . Defaults to datetime(0).
        end_date (_type_, optional): end od date interval. Defaults to datetime.today().

    Returns:
        pd.DataFrame: dataframe consisting of hours and count of videos
    """
    history_filtered = filter_videos_by_date('time', start_date, end_date, history)
    history_filtered['hours'] = history_filtered['time'].dt.hour
    hourly_count = history_filtered['hours'].value_counts().sort_index()
    hourly_count_df = pd.DataFrame(zip(list(hourly_count.index), list(hourly_count.values)), columns=['hour', 'count of videos'])
    return hourly_count_df


def average_video_duration(videos: data.Videos):
    return videos.content['duration'].mean()


def key_words_title():
    pass


def statistics_in_time(history: pd.DataFrame, videos: pd.DataFrame, ):
    watch_history = history.copy()
    years = set(watch_history['time'].dt.year)
    #watch_history_years = []
    years_analytics = pd.DataFrame(columns=['year', 'title', 'count', 'total_watch_time'])
    for year in years:
        start_date=pd.to_datetime(str(year))
        end_date=pd.to_datetime(str(year+1))-timedelta(days=1)
        filtered_by_year = filter_videos_by_date(column_name='time',
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 videos=watch_history)
        # merged = filtered_by_year.merge(videos, left_on='titleUrl', right_on='id')
        most_viewed_videos = show_most_viewed_videos(filtered_by_year, videos, count=1)
        total_watch_time = calculate_total_watch_time(filtered_by_year, videos)
        new_row = {'year': year, 'title': most_viewed_videos['title'].values[0], 'count': most_viewed_videos['count'].values[0],'total_watch_time': total_watch_time}
        years_analytics = pd.concat([years_analytics, pd.DataFrame([new_row])], ignore_index=True)
        # years_analytics = years_analytics.loc[len(years_analytics)] = new_row
        #watch_history_years.append(filtered_by_year)
    return years_analytics


def average_break():
    pass


def show_biggest_value_videos(column_name: str, history: pd.DataFrame, videos: pd.DataFrame, count: int = 10):
    merged = history.merge(videos, how='inner', left_on='titleUrl', right_on='id')
    columns_to_drop = set(merged.columns) - set([column_name, 'id', 'title'])
    merged = merged.drop_duplicates(subset='id')
    merged = filter_videos_by(column_name, merged, [None], True)
    merged[column_name] = merged[column_name].astype(float)
    merged = merged.sort_values(by=column_name, ascending=False).head(count)
    merged = merged.drop(columns=columns_to_drop)
    return merged
