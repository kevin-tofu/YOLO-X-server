import os
from typing import NamedTuple

VERSION = os.getenv('VERSION', 'v0'),
AUTHOR = os.getenv('AUTHOR', 'kevin')
APP_PORT = os.getenv('APP_PORT', 80)
PATH_DATA = os.getenv('PATH_DATA', './temp')
PATH_MODEL = os.getenv('PATH_MODEL', f"./model/yolo.onnx")
PATH_CATEGORIES = os.getenv('PATH_CATEGORIES', '')
IMSIZE_HEIGHT = int(os.getenv('IMSIZE_HEIGHT', '640'))
IMSIZE_WIDTH = int(os.getenv('IMSIZE_WIDTH', '640'))


class Config(NamedTuple):
    app_port: int
    path_model: str
    path_data: str
    path_categories: str
    imsize_height: int
    imsize_width: int
    

config_org = Config(
    APP_PORT,
    PATH_MODEL,
    PATH_DATA,
    PATH_CATEGORIES,
    IMSIZE_HEIGHT,
    IMSIZE_WIDTH
)
