from adapters import repository, file, youtube_api
from domain.model import WatchHistory, Videos, Channels
from service_layer import unit_of_work
import pandas as pd
import tqdm


class Bootstrap:
    def __init__(
        self,
        history_file: file.AbstractFile = file.JSONFIle(
            r'Backend\Refactored\files\history.json'),
        api=youtube_api.Youtube_API,
        uow=unit_of_work.SqLiteUnitOfWork(),
        watch_history=WatchHistory(
            file.JSONFIle(r'Backend\Refactored\files\history.json').read(), None),
        videos=Videos(),
        channels=Channels()
    ) -> None:
        self.history = history_file.read()
        self.api = api
        self.uow = uow
        self.watch_history = watch_history
        self.videos = videos
        self.channels = channels
        self.watch_history.load_history()

    def load_videos_from_DB_or_API(self) -> None:
        """Function to
        """
        with self.uow:
            print(self.watch_history.watch_history)
            video_urls = list(
                set(filter(None, self.watch_history.history['titleUrl'])))
            if self.uow.inspector.has_table('videos'):
                self.watch_history.add(self.uow.videos)
                new_urls = list(set(video_urls) -
                                set(self.videos.content['id']))
                if new_urls is not []:
                    self.get_videos_details_from_api(new_urls)
            else:
                self.get_videos_details_from_api(video_urls)
            self.sql.write('damaged_urls', self.damaged_urls)

    def get_videos_details_from_api(
            self,
            video_urls: list[str],
            api: youtube_api.Youtube_API,
            batch_size=50,
            damaged_urls: list[str] = []
    ) -> None:
        """Function downloading data with YT API and converting it into DataFrame

        Args:
            video_urls (list[str]): list of url to be sent to YT API
        """

        # maximum length of urls list for single quotation
        number_of_batches = len(video_urls) // batch_size + 1
        progess_bar = tqdm(total=number_of_batches,
                           desc='Downloading Videos Details', unit='item')
        for i in range(batch_size, len(video_urls), batch_size):
            urls_list = list(
                set(video_urls[i-batch_size:i])-set([x[0] for x in damaged_urls.values]))
            videos_data = api.get_videos_info(urls_list, self.youtube)
            # if videos_data == []:
            #     damaged_urls = pd.concat([damaged_urls, pd.DataFrame(
            #         urls_list, columns=['id'])], ignore_index=True)

            videos_converted = self.JSON_to_DataFrame(videos_data)

            self.videos.add(videos_converted)
            progess_bar.update(1)


def initialize():
    pass


def main():
    bootstrap = Bootstrap()
    bootstrap.load_videos_from_DB_or_API()
    print(bootstrap.videos)


if __name__ == '__main__':
    main()
