import os, sys
import io
from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
from fastapi import Response
from typing import List, Optional, Union

from PIL import Image
from controllers.detection import myProcessor
import MediaHandler
import cv2
import numpy as np
from config import config_org

test_config = dict(
    PATH_DATA = "./temp"
)

handler = MediaHandler.Router(
    myProcessor(config_org), 
    MediaHandler.Config(**test_config)
)
router = APIRouter(prefix="")

@router.post('/coco_image')
async def image(
    file: UploadFile = File(...), \
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    
    params = dict(
        test = test
    )
    print(file.filename)
    return await handler.post_file_BytesIO(
        "image-bytesio", \
        file, \
        bgtask, \
        **params
    )



@router.post('/coco_video')
async def video(
    file: UploadFile = File(...), \
    bgtask: BackgroundTasks = BackgroundTasks(),\
    test: Optional[int] = 0
):
    """
    """

    params = dict(
        test = test
    )
    return await handler.post_file("video", file, "json", bgtask, **params)

