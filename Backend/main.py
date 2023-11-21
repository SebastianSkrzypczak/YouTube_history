from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
import bootstrap


app = FastAPI()

templates = Jinja2Templates(directory="templates")

cache = {}

manager = bootstrap.initialize()


@app.get("/default")
async def read_all_default():
    content = {
        "total": manager.total_watch_time(),
        "most_viewed_videos": manager.most_viewed_videos(),
        "most_viewed_channels": manager.most_viewed_channels(),
        "time_activity": manager.time_activity(),
        "average": manager.averagee_video_duration(),
        "statistics": manager.statistics_in_time(),
        "most_liked_vidoes": manager.most_liked_vidoes(),
        "most_views_videos": manager.most_views_videos(),
    }

    return JSONResponse(content)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MostViewedVideosData(BaseModel):
    count: int
    categories: list[int]


@app.get("/total")
async def post_total_watch_time():
    return JSONResponse(manager.total_watch_time())


# @app.get("/most_viewed_videos")
# async def post_most_viewed_videos(data: MostViewedVideosData):
#     cache["most_viewed_videos"] = {"count": data.count, "categories": data.categories}
#     return {"message": "Date downloaded correct!"}


@app.get("/most_viewed_videos")
async def get_most_viewed_videos():
    if "count" in cache.keys():
        count = int(cache["most_viewed_videos"]["count"])
    else:
        count = 10
    if "categories" in cache.keys():
        categories = cache["most_viewed_videos"]["categories"]
    else:
        categories = []
    content = {
        "most_viewed_videos": manager.most_viewed_videos(
            count=count, excluded_categories=categories
        )
    }

    return JSONResponse(content)


@app.get("/most_viewed_channels")
async def read_most_viewed_channels():
    content = {"most_viewed_channels": manager.most_viewed_channels()}

    return JSONResponse(content)


@app.get("/time_activity")
async def read_time_activity():
    content = {
        "time_activity": manager.time_activity(),
    }

    return JSONResponse(content)


@app.get("/average")
async def read_average():
    content = {"average": manager.averagee_video_duration()}

    return JSONResponse(content)


@app.get("/statistics")
async def read_statistics():
    content = {
        "statistics": manager.statistics_in_time(),
    }

    return JSONResponse(content)


@app.get("/most_liked_vidoes")
async def read_most_liked_vidoes():
    content = {"most_liked_vidoes": manager.most_liked_vidoes()}

    return JSONResponse(content)


@app.get("/most_views_videos")
async def read_most_views_videos():
    content = {"most_views_videos": manager.most_views_videos()}

    return JSONResponse(content)


def main():
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
