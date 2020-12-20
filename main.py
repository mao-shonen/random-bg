import os
import random
import hashlib
from typing import Any, Dict, Optional
from time import time
from functools import lru_cache
from urllib.parse import urlencode
import httpx
import aiofiles
from pydantic import BaseSettings
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, FileResponse


class Config(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    cloudimg_io_token: str = None
    cloudimg_io_timeout: float = 300.0  # convert image timeout
    cloudimg_io_quality: int = 85
    image_dir: str = None
    cache_dir: str = './cache'
    cache_ttl: float = 300.0


config = Config()
if not all([config.cloudimg_io_token, config.image_dir]):
    raise Exception('缺少config')

app = FastAPI()


def getImageUrl(domain: str, img: str) -> str:
    return f'https://{config.cloudimg_io_token}.cloudimg.io/v7/{domain}/origin_img/{img}?' + urlencode(
        dict(
            func='crop',
            width=1920,
            height=1080,
            sharp=1,
            force_format='webp',
            q=config.cloudimg_io_quality,
        ))


#@lru_cache()
def md5(v: str) -> str:
    return hashlib.md5(v.encode()).hexdigest()


@lru_cache(maxsize=1)
def getImages(*, cache_ttl: Optional[Any] = None) -> Dict[str, str]:
    # cloudimg.io 如果缺少副檔有機率出現錯誤
    return {
        md5(f) + os.path.splitext(f)[1]: f
        for f in os.listdir(config.image_dir)
        if f.endswith(('.jpg', '.jpeg', '.jfif', '.png', '.bmp', '.ico',
                       '.gif', '.webp'))
    }


@app.get('/random')
async def _random():
    cache_ttl = int(time() / config.cache_ttl)
    img_hash = random.choice(list(getImages(cache_ttl=cache_ttl).keys()))
    url_path = f'/img/{img_hash}'
    return RedirectResponse(url_path, status_code=302)


@app.get('/imgs')
async def _list():
    return [dict(url=f'/img/{img_hash}') for img_hash in getImages().keys()]


@app.get('/demo')
async def _demo():
    return FileResponse('demo.html')


@app.get('/cache')
async def _cache():
    return FileResponse('cache.html')


@app.get('/img/{img_hash}')
async def _fetch(request: Request, img_hash: str):
    img_path = getImages().get(img_hash)
    if not img_path:
        raise HTTPException(404)

    cache_img_path = os.path.join(config.cache_dir, f'{img_hash}.webp')

    if not os.path.exists(cache_img_path):
        domain = request.headers.get('host', request.base_url.hostname)
        async with httpx.AsyncClient() as client:
            res = await client.get(getImageUrl(domain, img_hash),
                                   timeout=config.cloudimg_io_timeout)
            res.raise_for_status()

            tmp_file = cache_img_path + '.tmp'
            async with aiofiles.open(tmp_file, 'wb') as f:
                await f.write(res.read())

            os.rename(tmp_file, cache_img_path)

    return FileResponse(cache_img_path, media_type='image/webp')


@app.get('/origin_img/{img_hash}')
async def _origin_image(img_hash: str):
    img_path = getImages().get(img_hash)
    if not img_path:
        raise HTTPException(404)

    return FileResponse(os.path.join(config.image_dir, img_path))
