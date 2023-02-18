import os
from typing import NamedTuple

VERSION = os.getenv('VERSION', 'v0'),
AUTHOR = os.getenv('AUTHOR', 'kevin')
APP_PORT = os.getenv('APP_PORT', 80)
PATH_DATA = os.getenv('PATH_DATA', './temp')
PATH_MODEL = os.getenv('PATH_MODEL', f"./model/yolox_m.onnx")
PATH_CATEGORIES = os.getenv('PATH_CATEGORIES', '')


class Config(NamedTuple):
    app_port: int
    path_model: str
    path_data: str
    path_categories: str
    

config_org = Config(
    APP_PORT,
    PATH_MODEL,
    PATH_DATA,
    PATH_CATEGORIES
)
