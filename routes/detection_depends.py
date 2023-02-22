
from typing import Optional
from fastapi import FastAPI, Path, Query

async def params_detector(
    th_conf: Optional[float] = Query(0.5, gt=0.01, lt=0.99), \
    th_nms: Optional[float] = Query(0.5, gt=0.01, lt=0.99), \
    filter_cat: Optional[list[int]] = Query(None), \
    test: Optional[int] = None
) -> dict:
    
    print('filter_cat : ', filter_cat)
    ret = dict(
        th_conf = th_conf, \
        th_nms = th_nms, \
        filter_cat = filter_cat, \
        test = test
    )
    return ret