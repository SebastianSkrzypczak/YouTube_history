from domain.model import Videos
import pandas as pd
import json
from icecream import ic
from unittest.mock import patch


class Test_Videos:
    def test_add_successful(self):
        mock_json = [
            {
                "id": "test_id",
                "title": "test_title",
                "publishedAt": "test_publishedAt",
                "channelId": "test_channelId",
                "categoryId": "test_categoryId",
                "duration": "test_duration",
                "viewCount": "test_viewCount",
                "likeCount": "test_likeCount",
                "thumbnail": "test_thumbnail",
            }
        ]
        mock_data_frame = pd.DataFrame(mock_json)
        vidoes = Videos()
        vidoes.add(mock_data_frame)
        ic(vidoes.content)
        ic(mock_data_frame)
        assert vidoes.content.equals(mock_data_frame)

    def test_add_empty_frame(self):
        empty_data_frame = pd.DataFrame(
            columns=[
                "id",
                "title",
                "publishedAt",
                "channelId",
                "categoryId",
                "duration",
                "viewCount",
                "likeCount",
                "thumbnail",
            ]
        )
        videos = Videos()
        with patch("logging.debug") as mock_debug:
            videos.add(empty_data_frame)

        mock_debug.assert_called_once_with("empty videos data")
