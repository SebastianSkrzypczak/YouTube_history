import data
import logic


def main():
    history = data.WatchHistory()
    history.add()
    print(logic.calculate_total_watch_time(history.videos))
    print(logic.show_most_viewed_videos(history.videos))
    print(logic.show_most_viewed_channels(history.videos))
    print(logic.average_video_duration(history.videos))

if __name__ == '__main__':
    main()
