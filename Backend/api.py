from googleapiclient.discovery import build
import json

API_file = open('API.txt', 'r')
API_KEY = API_file.readline()

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_videos_info(video_ids) -> json:
    response = youtube.videos().list(part='snippet,contentDetails,statistics', id=','.join(video_ids)).execute()
    if response.get('items'):
        formatted_json = response.get('items')
        return formatted_json
    else:
        return []


def get_channels_info(channels_ids):
    response = youtube.channels().list(part='snippet,statistics,brandingSettings,contentDetails', id=','.join(channels_ids)).execute()
    if response.get('items'):
        formatted_json = response.get('items')
        return formatted_json
    else:
        return []


def main():
    print(get_videos_info(['hC8CH0Z3L54']))


if __name__ == '__main__':
    main()

# TODO: Exceptions and ErrorsHandlig