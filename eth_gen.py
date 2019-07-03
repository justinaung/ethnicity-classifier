from pathlib import Path
from io import BytesIO
import sys
import asyncio

from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastai.vision import open_image, load_learner
import torch
import uvicorn
import aiohttp


async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


app = Starlette()

learner = load_learner(Path.cwd())

@app.route('/upload', methods=['POST'])
async def upload(request):
    form = await request.form()
    data_file = await form['file'].read()
    return predict_image_from_data_file(data_file)


@app.route('/classify-url', methods=['GET'])
async def classify_url(request):
    data_file = await get_bytes(request.query_params['url']) 
    return predict_image_from_data_file(data_file)


def predict_image_from_data_file(data_file):
    img = open_image(BytesIO(data_file))
    losses = img.predict(learner)
    return JSONResponse({
        'predictions': sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })


@app.route('/')
def form(request):
    return HTMLResponse(
        """
        <form action="/upload" method="post" enctype="multipart/form-data">
            Select image to upload:
            <input type="file" name="file">
            <input type="submit" value="Upload Image">
        </form>
        Or submit a URL:
        <form action="/classify-url" method="get">
            <input type="url" name="url">
            <input type="submit" value="Fetch and analyze image">
        </form>
        """
    )


@app.route('/form')
def redirect_to_homepage(request):
    return RedirectResponse('/')


if __name__ == '__main__':
    if 'server' in sys.argv:
        uvicorn.run(app, host='0.0.0.0', port=8008)
