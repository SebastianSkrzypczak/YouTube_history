from googleapiclient.discovery import build
import json

API_file = open('API.txt', 'r')
API_KEY = API_file.readline()

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_videos_info(video_ids) -> json:
    #try:
    #print(video_ids)
    response = youtube.videos().list(part='snippet,contentDetails,statistics', id=','.join(video_ids)).execute()
    #except Exception:
    #print(f'fff: {response}')
        #return False
    if response.get('items'):
        formatted_json = response.get('items')
        return formatted_json
    else:
        return []


def get_channel_info():
    try:
        response = youtube.channels().list(part='snippet,statistics,brandingSettings,contentDetails', id='UCsFfolMaE4DsBATPVwu3pkQ').execute()
    except Exception:
        print('except')
    if response.get('items'):
        formatted_json = response.get('items')
        print(formatted_json)
    else:
        print('else')


def main():
    pass


if __name__ == '__main__':
    main()
