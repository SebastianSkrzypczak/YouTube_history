from api import get_videos_info, get_channels_info, set_up
from unittest.mock import mock_open, patch
import unittest
import pytest


def test_set_up_no_file():
    with patch('builtins.open', mock_open()) as m:
        m.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            set_up()


def test_set_up_invalid_key():
    with patch('builtins.open', mock_open(read_data='invalid_key')) as m:
        m.side_effect = Exception
        with pytest.raises(Exception):
            print(set_up())


def test_get_videos_info():
    video_id = ['hC8CH0Z3L54']
    channel_id = ['UCxqkOxQYocXRtSqlotgXh7w']
