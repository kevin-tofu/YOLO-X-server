
from typing import List, Optional
from fastapi import FastAPI, Path, Query

async def params_detector(
    th_conf: Optional[float] = Query(0.5, gt=0.01, lt=0.99), \
    th_nms: Optional[float] = Query(0.5, gt=0.01, lt=0.99), \
    test: Optional[int] = None
) -> dict:
    
    ret = dict(
        th_conf = th_conf, \
        th_nms = th_nms, \
        test = test
    )
    return ret