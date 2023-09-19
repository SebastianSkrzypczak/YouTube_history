import data
import logic


def main():
    history = data.WatchHistory()
    history.add()
    history.save()
    # print(history.watch_history)
    # print(history.videos.content)
    # print(logic.calculate_total_watch_time(history.watch_history, history.videos.content))
    # print('\n')
    # print(logic.show_most_viewed_videos(history.watch_history, history.videos.content, count=10, excluded_categories=[]))
    # print('\n')
    # print(logic.show_most_viewed_channels(history.watch_history))
    # plots.draw(logic.time_activity_analysis(history.watch_history), xlabel='Hours', ylabel='Watched vidoes', title='Watched videos by hours')
    # print(logic.average_video_duration(history.videos))
    print('\n')
    # print(logic.any_analysis('channelId', history.watch_history, history.videos.content))
    print(logic.statistics_in_time(history.watch_history, history.videos.content))
    print('\n')



if __name__ == '__main__':
    main()

# TODO: multiprocessing
