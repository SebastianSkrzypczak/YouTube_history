from googleapiclient.discovery import build
import json

API_KEY = "AIzaSyDZy2mt02c9BIegzOurTrQpOBl_dqmunh0"

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_info(video_id):
    try:
        response = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id).execute()
    except Exception:
        print('except')
    if response.get('items'):
        formatted_json = json.dumps(response, indent=4)
        return formatted_json
    else:
        print('else')


def get_channel_info():
    try:
        response = youtube.channels().list(part='snippet,statistics,brandingSettings,contentDetails', id='UCsFfolMaE4DsBATPVwu3pkQ').execute()
    except Exception:
        print('except')
    if response.get('items'):
        formatted_json = json.dumps(response, indent=4)
        print(formatted_json)
    else:
        print('else')


def main():
    video_id = 'axwE9q7llEQ'
    video_info = get_video_info(video_id)
    print(get_channel_info())

if __name__ == '__main__':
    main()

