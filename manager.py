import data
import logic
import json
from icecream import ic


class Logic:
    def __init__(self) -> None:
        self.history = data.WatchHistory()
        self.history.add()
        self.history.save()
        self.watch_history = self.history.watch_history
        self.content = self.history.videos.content

    @property
    def total_watch_time(self):
        print(json.dumps(logic.calculate_total_watch_time(self.history.watch_history, self.history.videos.content)))
        return json.dumps(logic.calculate_total_watch_time(self.history.watch_history, self.history.videos.content))

    @property
    def most_viewed_videos(self):
        return logic.show_most_viewed_videos(self.history.watch_history, self.history.videos.content, count=10, excluded_categories=[]).to_json()

    @property
    def most_viewed_channels(self):
        return logic.show_most_viewed_channels(self.history.watch_history, self.history.videos.content).to_json()

    @property
    def averagee_video_duration(self):
        return json.dumps(logic.average_video_duration(self.history.videos))

    @property
    def statistics_in_time(self):
        return logic.statistics_in_time(self.history.watch_history, self.history.videos.content).to_json()

    # plots.draw(logic.time_activity_analysis(history.watch_history), xlabel='Hours', ylabel='Watched vidoes', title='Watched videos by hours')
    # print(logic.any_analysis('channelId', history.watch_history, history.videos.content))


logic_ = Logic()


def main():
    print(logic_.most_viewed_videos)


if __name__ == '__main__':
    main()

# TODO: multiprocessing
