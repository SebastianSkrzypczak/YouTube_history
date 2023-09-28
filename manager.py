import data
import logic
import json


class Logic:
    """A class to handle backend logic and converting returned data to JSON 
    """

    def __init__(self) -> None:
        self.history = data.WatchHistory()
        self.history.add()
        self.history.save()
        self.watch_history = self.history.watch_history
        self.content = self.history.videos.content

    def total_watch_time(self) -> json:
        """Function to handle total watch time query

        Returns:
            json: {'total_watch_time': float = seconds}
        """
        data = {'total_watch_time': json.dumps(logic.calculate_total_watch_time(self.history.watch_history, self.history.videos.content))}
        return json.dumps(data)

    def most_viewed_videos(self, count = 10, excluded_categories = []) -> json:
        """Function to handle most viewed videos query

        Returns:
            json: {'id': str
                   'count': int
                   'title': str
                   }
        """
        return logic.show_most_viewed_videos(self.history.watch_history, self.history.videos.content, count=count, excluded_categories=excluded_categories).to_json(orient='records')

    def most_viewed_channels(self) -> json:
        """Function to handle most viewed channels query

        Returns:
            json: {'channelId': int = count of viewes}
        """
        return logic.show_most_viewed_channels(self.history.watch_history, self.history.videos.content).to_json(orient='records')

    def time_activity(self) -> json:
        """Function to hadnle time activity query:

        Returns:
            json: _description_
        """
        return logic.time_activity_analysis(self.history.watch_history).to_json(orient='records')

    def averagee_video_duration(self) -> json:
        """Function to handle average video duration query

        Returns:
            json: {'average_video_duration': float = seconds
        """
        data = {'average_video_duration': logic.average_video_duration(self.history.videos)}
        return json.dumps(data)

    def statistics_in_time(self) -> json:
        """Function to handle statistics in time query

        Returns:
            json: {'year': int,
                   'title': str,
                   'count': int,
                   'total_watch_time': float = seconds
                  }
        """
        return logic.statistics_in_time(self.history.watch_history, self.history.videos.content).to_json(orient='records')

    def most_liked_vidoes(self):
        return logic.show_biggest_value_videos('likeCount', self.history.watch_history, self.history.videos.content).to_json(orient='records')

    def most_views_videos(self):
        return logic.show_biggest_value_videos('viewCount', self.history.watch_history, self.history.videos.content).to_json(orient='records')


logic_ = Logic()


def main():
    pass


if __name__ == '__main__':
    main()

# TODO: filtering
# TODO: not properties 
# TODO: most viewed channels returns wrong values
