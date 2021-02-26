from pydantic import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    source_dir: str = './images'
    source_regex: str = r'\.(?:jpe?g|jfif|png|bmp|gif|webp|ico)$'
    source_cache_ttl: float = 300.0

    image_width: int = 1920
    image_height: int = 1080
    image_quality: int = 85
    image_auto_webp: bool = True


config = Config()
