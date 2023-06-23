from fastapi import APIRouter, File, UploadFile, Header, Depends
from fastapi import BackgroundTasks
from typing import Optional, Union

from controllers.detection import myProcessor
import filerouter
from config import config_org
from filerouter import processType
from routes.detection_depends import params_detector, params_model

test_config = dict(
    data_path = "./temp"
)

handler = filerouter.router(
    myProcessor(config_org), 
    filerouter.config(**test_config)
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
    file: UploadFile = File(...),
    bgtask: BackgroundTasks = BackgroundTasks(),
    params: dict = Depends(params_model)
):  
    """
    """
    
    return await handler.post_file(
        "patch-model",
        processType.FILE,
        file,
        None,
        bgtask=bgtask,
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
    file: UploadFile = File(...),
    # bgtask: BackgroundTasks = BackgroundTasks(),
    params: dict = Depends(params_detector)
):  
    """
    """
    
    return await handler.post_file(
        "image",
        processType.BYTESIO,
        file,
        None,
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

    # return await handler.post_file(
    #     "video", 
    #     file, 
    #     "json", 
    #     bgtask, 
    #     **params
    # )
    return await handler.post_file(
        "video",
        processType.FILE,
        file,
        None,
        bgtask=bgtask,
        **params
    )

@router.post("/coco_image/")
async def redirect_coco_image(
    file: UploadFile = File(...),
    bgtask: BackgroundTasks = BackgroundTasks(),
    params: dict = Depends(params_detector)
):
    return await handler.post_file(
        "image",
        processType.BYTESIO,
        file,
        None,
        bgtask=bgtask,
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
        processType.FILE,
        file,
        None,
        bgtask=bgtask,
        **params
    )

@router.get("/categories/")
async def redirect_categories():
    return handler.processor.get_categories()
