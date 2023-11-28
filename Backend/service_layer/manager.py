"""This module defines the `Manager` class, which handles backend logic and converts returned data to JSON."""

import json
from domain.model import Videos, WatchHistory
from service_layer import logic


class Manager:
    """A class to handle backend logic and converting returned data to JSON"""

    def __init__(self, history: WatchHistory, videos: Videos) -> None:
        self.history = history.history
        self.videos = videos.content

    def total_watch_time(self) -> json:
        """Function to handle total watch time query

        Returns:
            json: {'total_watch_time': float = seconds}
        """
        data = {
            "total_watch_time": json.dumps(
                logic.calculate_total_watch_time(self.history, self.videos)
            )
        }
        return data  # json.dumps(data)

    def most_viewed_videos(self, count: int = 10, excluded_categories=[]) -> json:
        """Function to handle most viewed videos query

        Returns:
            json: {'id': str
                   'count': int
                   'title': str
                   }
        """
        return logic.show_most_viewed_videos(
            self.history,
            self.videos,
            count=count,
            excluded_categories=excluded_categories,
        ).to_dict(
            orient="records"
        )  # .to_json(orient='records')

    def most_viewed_channels(self) -> json:
        """Function to handle most viewed channels query

        Returns:
            json: {'channelId': int = count of viewes}
        """
        return logic.show_most_viewed_channels(self.history, self.videos).to_dict(
            orient="records"
        )

    def time_activity(self) -> json:
        """Function to hadnle time activity query:

        Returns:
            json: _description_
        """
        return logic.time_activity_analysis(self.history).to_dict(orient="records")

    def averagee_video_duration(self) -> json:
        """Function to handle average video duration query

        Returns:
            json: {'average_video_duration': float = seconds
        """
        data = {"average_video_duration": logic.average_video_duration(self.videos)}
        return data

    def statistics_in_time(self) -> json:
        """Function to handle statistics in time query

        Returns:
            json: {'year': int,
                   'title': str,
                   'count': int,
                   'total_watch_time': float (in seconds)
                  }
        """
        return logic.statistics_in_time(self.history, self.videos).to_dict(
            orient="records"
        )

    def most_liked_vidoes(self, count=10) -> json:
        """Fuction to handle videos with most likes count query

        Args:
            count (int, optional): Quantity of most liked videos. Defaults to 10.

        Returns:
            json:  {'id': str,
                   'title': str,
                   'like_count': float,
                   }
        """
        return logic.show_biggest_value_videos(
            "likeCount",
            self.history,
            self.videos,
            count=count,
        ).to_dict(orient="records")

    def most_views_videos(self, count=10) -> json:
        """FUnction to handle videos with most view count query

        Args:
            count (int, optional): Quantity of most viewed videos. Defaults to 10.

        Returns:
            json: {'id': str,
                   'title': str,
                   'view_count': float,
                   }
        """
        return logic.show_biggest_value_videos(
            "viewCount", self.history, self.videos, count
        ).to_dict(orient="records")


def main():
    pass


if __name__ == "__main__":
    main()
