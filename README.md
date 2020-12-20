# random-bg

~~又是一個沒找到合用的開源專案只好自己做系列~~  
一個簡單的隨機背景圖  
在我家的NAS上執行

效果範例網址 `random-bg.maou.app/demo`

> 圖片轉換使用 [cloudimage.io](https://cloudimage.io)
> 使用需註冊一個cloudimage.io帳號


## 安裝

* python >= 3.7
* [poetry](https://github.com/python-poetry/poetry)

```bash
poetry install
```

## 配置 dotenv

`vim .env`

```conf
cloudimg_io_token={cloudimg.io拿到的token}
image_dir={圖片資料夾}
```

## 執行

[uvicorn](https://www.uvicorn.org)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
