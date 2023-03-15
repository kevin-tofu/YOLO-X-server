import os, sys
import io
from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
from fastapi import Response
from typing import Optional, Union

from PIL import Image
from controllers.detection import myProcessor
import mediarouter
import cv2
import numpy as np
from config import config_org

from routes.detection_depends import params_detector, params_model

test_config = dict(
    PATH_DATA = "./temp"
)

handler = mediarouter.router(
    myProcessor(config_org), 
    mediarouter.config(**test_config)
)
router = APIRouter(prefix="")

@router.get('/model-info')
async def get_model_info(
):  
    """
    """
    return handler.processor.get_model_info()

@router.patch('/model')
async def patch_model(
    file: UploadFile = File(...), \
    bgtask: BackgroundTasks = BackgroundTasks(),\
    params: dict = Depends(params_model)
):  
    """
    """
    
    return await handler.post_file(
        "patch-model", \
        file, \
        bgtask=bgtask, \
        **params
    )

@router.get('/categories')
async def get_categories(
):  
    """
    """
    
    return handler.processor.get_categories()

@router.post('/coco_image')
async def image(
    file: UploadFile = File(...), \
    bgtask: BackgroundTasks = BackgroundTasks(),\
    params: dict = Depends(params_detector)
):  
    """
    """
    
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
    params: dict = Depends(params_detector)
):
    """
    """

    return await handler.post_file(
        "video", 
        file, 
        "json", 
        bgtask, 
        **params
    )

@router.post("/coco_image/")
async def redirect_coco_image(
    file: UploadFile = File(...), \
    bgtask: BackgroundTasks = BackgroundTasks(),\
    params: dict = Depends(params_detector)
):
    return await handler.post_file_BytesIO(
        "image-bytesio", \
        file, \
        bgtask, \
        **params
    )

@router.post("/coco_video/")
async def redirect_coco_video(
    file: UploadFile = File(...), \
    bgtask: BackgroundTasks = BackgroundTasks(),\
    params: dict = Depends(params_detector)
):
    return await handler.post_file(
        "video", 
        file, 
        "json", 
        bgtask, 
        **params
    )
@router.get("/categories/")
async def redirect_categories():
    return handler.processor.get_categories()
