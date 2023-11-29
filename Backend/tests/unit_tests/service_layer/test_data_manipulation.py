from service_layer.data_manipulation import (
    iso8601_to_seconds,
    extract_any,
    JSON_to_DataFrame,
)
import pandas as pd
import pytest
import json


class Test_iso8601_to_seconds:
    def test_basic_case(self):
        time = "PT1H30M"
        result = iso8601_to_seconds(time)
        assert result == (30.0 * 60 + 60.0 * 60)

    def test_case_without_days(self):
        time = "PT3H45M"
        result = iso8601_to_seconds(time)
        assert result == (45.0 * 60 + 3 * 60 * 60)

    def test_case_with_days(self):
        time = "P2DT3H45M"
        result = iso8601_to_seconds(time)
        assert result == (45.0 * 60 + 3 * 60 * 60 + 2 * 24 * 60 * 60)

    def test_case_with_only_days(self):
        time = "P5D"
        result = iso8601_to_seconds(time)
        assert result == (5 * 24 * 60 * 60)

    def test_case_with_only_hours(self):
        time = "PT6H"
        result = iso8601_to_seconds(time)
        assert result == (6 * 60 * 60.0)

    def test_case_with_only_minutes(self):
        time = "PT45M"
        result = iso8601_to_seconds(time)
        assert result == (45 * 60.0)

    def test_case_with_only_seconds(self):
        time = "PT120S"
        result = iso8601_to_seconds(time)
        assert result == (120)

    def test_case_with_all_units(self):
        time = "P3DT4H15M30S"
        result = iso8601_to_seconds(time)
        assert result == (274530)

    def test_case_with_empty_input(self):
        time = ""
        with pytest.raises(ValueError):
            result = iso8601_to_seconds(time)

    def test_case_with_invalid_format(self):
        time = "ABC"
        with pytest.raises(ValueError):
            result = iso8601_to_seconds(time)

    def test_case_with_whitespace(self):
        time = "  PT2H  "
        with pytest.raises(ValueError):
            result = iso8601_to_seconds(time)

    def test_case_with_lowercase_letters(self):
        time = "pt2h30m"
        with pytest.raises(ValueError):
            result = iso8601_to_seconds(time)

    def test_case_with_negative_values(self):
        time = "-PT2H30M"
        with pytest.raises(ValueError):
            result = iso8601_to_seconds(time)


class Test_extract_any:
    def test_extract_any_successful(self):
        json_str = '{"key1": "value1", "key2": "value2"}'
        json_dict = json.loads(json_str)
        extracted = extract_any(json_dict, "key1")
        assert extracted == "value1"


class Test_JSON_to_DataFrame:
    def test_case_successful_path(self):
        json_data = json.loads(
            r"""{
      "kind": "youtube#video",
      "etag": "oTn7pu_bOedYn2f97iBurXdP1_A",
      "id": "Ks-_Mh1QhMc",
      "snippet": {
        "publishedAt": "2012-10-01T15:27:35Z",
        "channelId": "UCAuUUnT6oDeKwE6v1NGQxug",
        "title": "Your body language may shape who you are | Amy Cuddy",
        "description": "Body language affects how others see us, but it may also change how we see ourselves. Social psychologist Amy Cuddy argues that \"power posing\" -- standing in a posture of confidence, even when we don't feel confident -- can boost feelings of confidence, and might have an impact on our chances for success. (Note: Some of the findings presented in this talk have been referenced in an ongoing debate among social scientists about robustness and reproducibility. Read Amy Cuddy's response here: http://ideas.ted.com/inside-the-debate-about-power-posing-a-q-a-with-amy-cuddy/)\n\nGet TED Talks recommended just for you! Learn more at https://www.ted.com/signup.\n\nThe TED Talks channel features the best talks and performances from the TED Conference, where the world's leading thinkers and doers give the talk of their lives in 18 minutes (or less). Look for talks on Technology, Entertainment and Design -- plus science, business, global issues, the arts and more.\n\nFollow TED on Twitter: http://www.twitter.com/TEDTalks\nLike TED on Facebook: https://www.facebook.com/TED\n\nSubscribe to our channel: https://www.youtube.com/TED",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/hqdefault.jpg",
            "width": 480,
            "height": 360
          },
          "standard": {
            "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/sddefault.jpg",
            "width": 640,
            "height": 480
          },
          "maxres": {
            "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/maxresdefault.jpg",
            "width": 1280,
            "height": 720
          }
        },
        "channelTitle": "TED",
        "tags": [
          "Amy Cuddy",
          "TED",
          "TEDTalk",
          "TEDTalks",
          "TED Talk",
          "TED Talks",
          "TEDGlobal",
          "brain",
          "business",
          "psychology",
          "self",
          "success"
        ],
        "categoryId": "22",
        "liveBroadcastContent": "none",
        "defaultLanguage": "en",
        "localized": {
          "title": "Your body language may shape who you are | Amy Cuddy",
          "description": "Body language affects how others see us, but it may also change how we see ourselves. Social psychologist Amy Cuddy argues that \"power posing\" -- standing in a posture of confidence, even when we don't feel confident -- can boost feelings of confidence, and might have an impact on our chances for success. (Note: Some of the findings presented in this talk have been referenced in an ongoing debate among social scientists about robustness and reproducibility. Read Amy Cuddy's response here: http://ideas.ted.com/inside-the-debate-about-power-posing-a-q-a-with-amy-cuddy/)\n\nGet TED Talks recommended just for you! Learn more at https://www.ted.com/signup.\n\nThe TED Talks channel features the best talks and performances from the TED Conference, where the world's leading thinkers and doers give the talk of their lives in 18 minutes (or less). Look for talks on Technology, Entertainment and Design -- plus science, business, global issues, the arts and more.\n\nFollow TED on Twitter: http://www.twitter.com/TEDTalks\nLike TED on Facebook: https://www.facebook.com/TED\n\nSubscribe to our channel: https://www.youtube.com/TED"
        },
        "defaultAudioLanguage": "en"
      },
      "contentDetails": {
        "duration": "PT21M3S",
        "dimension": "2d",
        "definition": "hd",
        "caption": "true",
        "licensedContent": true,
        "contentRating": {},
        "projection": "rectangular"
      },
      "statistics": {
        "viewCount": "23990451",
        "likeCount": "406764",
        "favoriteCount": "0",
        "commentCount": "9597"
      }
    }"""
        )
        expected = pd.DataFrame(
            [
                {
                    "id": "Ks-_Mh1QhMc",
                    "title": "Your body language may shape who you are | Amy Cuddy",
                    "publishedAt": "2012-10-01T15:27:35Z",
                    "channelId": "UCAuUUnT6oDeKwE6v1NGQxug",
                    "categoryId": "22",
                    "duration": 1263.0,
                    "viewCount": "23990451",
                    "likeCount": "406764",
                    "thumbnail": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/sddefault.jpg",
                }
            ]
        )
        expected["publishedAt"] = pd.to_datetime(
            expected["publishedAt"], format="mixed"
        )
        result = JSON_to_DataFrame(json_data)

        assert result.equals(expected)
