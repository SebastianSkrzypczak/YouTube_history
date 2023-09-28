from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from manager import logic_
import logging
from icecream import ic

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def read_item(request: Request):
    context = {'request': request,
               'response': {'total': logic_.total_watch_time(),
               'most_viewed_videos': logic_.most_viewed_videos(),
               'most_viewed_channels': logic_.most_viewed_channels(),
               'time_activity': logic_.time_activity(),
               'average': logic_.averagee_video_duration(),
               'statistics': logic_.statistics_in_time(),
               'most_liked_vidoes': logic_.most_liked_vidoes(),
               'most_views_videos': logic_.most_views_videos(),}
               }

    logger = logging.getLogger(__name__)
    logger.info(context['response'])

    return templates.TemplateResponse('index.html', context)


def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
