from adapters.youtube_api import Youtube_API
from googleapiclient.discovery import Resource
from unittest.mock import patch, mock_open
import pytest
from json import JSONDecodeError, loads
from icecream import ic
import requests


def test_set_up_successful_path():
    api = Youtube_API()
    assert type(api.youtube) is Resource


def test_set_up_error_no_API_file():
    wrong_file = "wrong_file.txt"
    with pytest.raises(FileNotFoundError):
        api = Youtube_API(file_path=wrong_file)


def test_set_up_error_wrong_api_key():
    invalid_api_key = "invalid_api_key"
    with patch("builtins.open", mock_open(read_data=invalid_api_key)):
        with pytest.raises(JSONDecodeError):
            api = Youtube_API()


def test_get_videos_info_successful_path():
    with open("API.txt", "r") as file:
        api_key = file.readline()
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=Ks-_Mh1QhMc%2Cc0KYU2j0TM4%2CeIho2S0ZahI&key={api_key}"
    http_response = requests.get(url=url)
    http_response = loads(http_response.content.decode("utf-8")).get("items")
    api = Youtube_API()
    assert http_response == api.get_videos_info(
        ["Ks-_Mh1QhMc", "c0KYU2j0TM4", "eIho2S0ZahI"]
    )
