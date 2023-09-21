from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from manager import logic_

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def read_item(request: Request):
    context = {'request': request, 'total': logic_.statistics_in_time}
    return templates.TemplateResponse('index.html', context)


def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
