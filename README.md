# random-bg

~~又是一個沒找到合用的開源專案只好自己做系列~~  
一個簡單的隨機背景圖  
在我家的NAS上執行

效果範例網址 `random-bg.maou.app/demo`

~~> 圖片轉換使用 [cloudimage.io](https://cloudimage.io)~~
~~> 使用需註冊一個cloudimage.io帳號~~

更換為 [statically.io](https://statically.io)

## 安裝

* python >= 3.7
* [poetry](https://github.com/python-poetry/poetry)

```bash
poetry install
```

## 配置 dotenv

`vim .env`

可用參數參考 `config.py`

```conf
source_dir={圖片資料夾}
image_quality={圖片品質}
```

## 執行

[uvicorn](https://www.uvicorn.org)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 從 docker 執行

```bash
docker run -it \
  --name random-bg \
  -v /data/photos:/app/images:ro \
  -p 8080:80 \
  q267009886/random-bg
```
