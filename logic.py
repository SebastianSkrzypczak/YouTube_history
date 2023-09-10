import data


def calculate_total_watch_time(videos: data.Videos):
    return videos.content['duration'].sum()


def show_most_viewed_videos(videos: data.Videos):
    most_viewed = videos.content['id'].value_counts().idxmax()
    view_count = videos.content['id'].value_counts().max()
    return most_viewed, view_count


def show_most_viewed_channels(videos: data.Videos):
    most_viewed = videos.content['channelId'].value_counts().idxmax()
    view_count = videos.content['channelId'].value_counts().max()
    return most_viewed, view_count


def time_activity_analysis():
    '''On what time You watch the most movies'''
    pass


def category_analysis():
    '''Which cattegories are watched the most + in time + %'''
    pass


def average_video_duration(videos: data.Videos):
    return videos.content['duration'].mean()


def key_words_title():
    pass


def statistics_in_time():
    pass


def average_break():
    pass
