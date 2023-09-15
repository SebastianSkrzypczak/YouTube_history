import data
import logic
import plots


def main():
    history = data.WatchHistory()
    history.add()
    history.save()
    #print(history.watch_history)
    #print(history.videos.content)
    print(logic.calculate_total_watch_time(history, history.videos))
    print('\n')
    print(logic.show_most_viewed_videos(history, history.videos, 10))
    print('\n')
    print(logic.show_most_viewed_channels(history))
    #plots.draw(logic.time_activity_analysis(history), xlabel='Hours', ylabel='Watched vidoes', title='Watched videos by hours')
    #print(logic.average_video_duration(history.videos))

if __name__ == '__main__':
    main()

# TODO: multiprocessing
