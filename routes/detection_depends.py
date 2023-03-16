
from typing import Optional
from fastapi import FastAPI, Path, Query

async def params_detector(
    th_conf: Optional[float] = Query(0.5, gt=0.01, lt=0.99), \
    th_nms: Optional[float] = Query(0.5, gt=0.01, lt=0.99), \
    categories: Optional[list[int]] = Query(None), \
    test: Optional[int] = None
) -> dict:
    
    # print('categories : ', categories)
    ret = dict(
        th_conf = th_conf, \
        th_nms = th_nms, \
        categories = categories, \
        test = test
    )
    return ret

async def params_model(
    imsize: Optional[list[int]] = Query(None), \
    test: Optional[int] = None
) -> dict:
    
    ret = dict(
        imsize=imsize,
        test = test
    )
    return ret