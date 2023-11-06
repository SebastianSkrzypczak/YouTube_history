from googleapiclient.discovery import build
import json


def set_up():
    try:
        api_file = open('API.txt', 'r')
    except FileNotFoundError as e:
        raise e
    API_KEY = api_file.readline()
    try:
        return build('youtube', 'v3', developerKey=API_KEY)
    except Exception as e:
        raise e


def get_videos_info(video_ids, youtube) -> json:
    response = youtube.videos().list(part='snippet,contentDetails,statistics',
                                     id=','.join(video_ids)).execute()
    if response.get('items'):
        formatted_json = response.get('items')
        return formatted_json
    else:
        return []


def get_channels_info(channels_ids, youtube):

    response = youtube.channels().list(part='snippet,statistics,brandingSettings,contentDetails',
                                       id=','.join(channels_ids)).execute()
    if response.get('items'):
        formatted_json = response.get('items')
        return formatted_json
    else:
        return []


def main():
    pass


if __name__ == '__main__':
    main()
