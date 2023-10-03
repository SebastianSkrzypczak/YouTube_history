from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
from manager import logic_
import logging

app = FastAPI()

templates = Jinja2Templates(directory='templates')

cache = {}


@app.get('/default')
async def read_all_default():
    content = {
               'total': logic_.total_watch_time(),
               'most_viewed_videos': logic_.most_viewed_videos(),
               'most_viewed_channels': logic_.most_viewed_channels(),
               'time_activity': logic_.time_activity(),
               'average': logic_.averagee_video_duration(),
               'statistics': logic_.statistics_in_time(),
               'most_liked_vidoes': logic_.most_liked_vidoes(),
               'most_views_videos': logic_.most_views_videos()
               }

    logger = logging.getLogger(__name__)
    logger.info(content)
    # TODO: logging

    return JSONResponse(content)


class MostViewedVideosData(BaseModel):
    count: int
    categories: list[int]


@app.post('/most_viewed_videos')
async def post_most_viewed_videos(data: MostViewedVideosData):

    cache['most_viewed_videos'] = {'count': data.count,
                                   'categories': data.categories}
    return {"message": "Date downloaded correct!"}


@app.get('/most_viewed_videos')
async def get_most_viewed_videos():
    if 'count' in cache.keys():
        count = int(cache['most_viewed_videos']['count'])
    else:
        count = 10
    if 'categries' in cache.keys():
        categories = cache['most_viewed_videos']['categories']
    else:
        categories = []
    content = {'most_viewed_videos': logic_.most_viewed_videos(count=count, excluded_categories=categories)}

    return JSONResponse(content)


@app.get('/most_viewed_channels')
async def read_most_viewed_channels():
    content = {'most_viewed_channels': logic_.most_viewed_channels()}

    return JSONResponse(content)


@app.get('/time_activity')
async def read_time_activity():
    content = {'time_activity': logic_.time_activity(),}

    return JSONResponse(content)


@app.get('/average')
async def read_average():
    content = {'average': logic_.averagee_video_duration()}

    return JSONResponse(content)


@app.get('/statistics')
async def read_statistics():
    content = {'statistics': logic_.statistics_in_time(),}

    return JSONResponse(content)


@app.get('/most_liked_vidoes')
async def read_most_liked_vidoes():
    content = {'most_liked_vidoes': logic_.most_liked_vidoes()}

    return JSONResponse(content)


@app.get('/most_views_videos')
async def read_most_views_videos():
    content = {'most_views_videos': logic_.most_views_videos()}

    return JSONResponse(content)


def main():
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
