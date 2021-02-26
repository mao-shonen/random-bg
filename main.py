import os
import re
from typing import Any, Dict
from time import time
from random import choice
from functools import lru_cache
from hashlib import md5
from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import RedirectResponse, FileResponse
from config import config


app = FastAPI()


def getImages() -> Dict[str, str]:
    @lru_cache(maxsize=1)
    def _(*, cache_key: Any):
        result = {}
        for img in filter(re.compile(config.source_regex).search, os.listdir(config.source_dir)):
            img_ext = os.path.splitext(img)[1]
            img_hash = md5(img.encode()).hexdigest()
            result[f'{img_hash}{img_ext}'] = img

        return result

    return _(cache_key=int(time() / config.source_cache_ttl))


@app.get('/random')
async def getRandom(request: Request):
    imgs = getImages()
    if len(imgs) == 0:
        raise HTTPException(404)

    rnd_img = choice(list(imgs.keys()))
    domain = request.headers.get('host', request.base_url.hostname)

    options = f'w={config.image_width},h={config.image_height},q={config.image_quality}'
    if config.image_auto_webp:
        options += ',f=auto'
    
    url_path = f'https://cdn.statically.io/img/{domain}/{options}/img/{rnd_img}'
    return RedirectResponse(url_path, status_code=302)


@app.get('/img/{img_hash}')
async def getImage(
        img_hash: str = Path(...)
    ):
    img = getImages().get(img_hash)
    if not img:
        raise HTTPException(404)

    img_path = os.path.join(config.source_dir, img)
    return FileResponse(img_path)


@app.get('/demo')
async def getDemoPage():
    return FileResponse(os.path.join('examlpe', 'index.html'))
