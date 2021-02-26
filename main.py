import os
import re
from typing import Any, List
from time import time
from random import choice
from functools import lru_cache
from urllib.parse import quote
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from config import config


app = FastAPI()
app.mount('/img', StaticFiles(directory=config.source_dir))


def getImages() -> List[str]:
    @lru_cache(maxsize=1)
    def _(*, cache_key: Any):
        regex = re.compile(config.source_regex)
        return list(filter(regex.search, os.listdir(config.source_dir)))

    return _(cache_key=int(time() / config.source_cache_ttl))


@app.get('/random')
async def getRandom(request: Request):
    imgs = getImages()
    if len(imgs) == 0:
        raise HTTPException(404)

    rnd_img = choice(imgs)
    domain = request.headers.get('host', request.base_url.hostname)

    options = f'w={config.image_width},h={config.image_height},q={config.image_quality}'
    if config.image_auto_webp:
        options += ',f=auto'
    
    url_path = f'https://cdn.statically.io/img/{domain}/{options}/img/{quote(rnd_img)}'
    return RedirectResponse(url_path, status_code=302)


@app.get('/demo')
async def getDemoPage():
    return FileResponse(os.path.join('examlpe', 'demo.html'))
