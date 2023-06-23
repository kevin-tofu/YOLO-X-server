import io
from typing import Optional
import json
import PIL
from PIL import Image
import numpy as np
import cv2
import onnxruntime as ort
import filerouter
from typing import NamedTuple, Literal
from controllers import functions as func
import coco_formatter
from config import Config
from fastapi import BackgroundTasks
from logconf import mylogger
logger = mylogger(__name__)


class myProcessor(filerouter.processor):
    def __init__(self, cfg: Config):
        super().__init__()

        self.cfg = cfg
        self.load_model(cfg.path_model)
        self.imsize = (cfg.imsize_height, cfg.imsize_width)
        if cfg.path_categories == '' or cfg.path_categories == 'coco':
            self.load_categories()
        else:
            self.load_categories(cfg.path_categories)
        
        # print(self.categories, len(self.categories))
        self.cvt_catid = lambda catid: self.categories[catid]['id']

    def load_model(self, path_model: str):
        ort_session = ort.InferenceSession(path_model)
        ort_session.get_modelmeta()
        # input_name = ort_session.get_inputs()
        # output_name = ort_session.get_outputs()
        self.session = ort_session

    def load_categories(self, fpath: Optional[str]=None):
        if fpath is None:
            self.categories = coco_formatter.get_categories()
        else:
            with open(cfg.path_categories, 'rb') as f:
                self.categories = json.load(f)

    def get_model_info(self):
        return dict(
            path_model=self.cfg.path_model
        )

    def patch_model(
        self, 
        path_model: str,
        **kwargs
    ):
        # del self.session
        # with open(self.cfg.path_model, 'wb') as f:
        #     f.write(fBytesIO)
        # self.load_model(self.cfg.path_model)
        self.load_model(path_model)
        if 'imsize' in kwargs:
            if type(kwargs['imsize']) is list:
                assert len(kwargs['imsize']) == 2
                self.imsize = kwargs['imsize']
                print(self.imsize, kwargs['imsize'])
        
    def get_categories(self):
        return self.categories


    async def post_file_process(
        self,
        process_name: str,
        data: filerouter.fileInfo | list[filerouter.fileInfo],
        file_dst_path: Optional[str] = None,
        bgtask: BackgroundTasks=BackgroundTasks(),
        **kwargs
    ):
        logger.info(f"process - {process_name}")
        if process_name == 'image':
            return await self.coco_image(
                data.bytesio,
                data.name,
                **kwargs
            )
        elif process_name == 'video':
            ret = func.detection_video(
                self.session,
                data.path,
                (640, 640),
                convert_catid=self.cvt_catid,
                th_conf = kwargs['th_conf'],
                th_nms = kwargs['th_nms'],
                categories = kwargs['categories']
            )

            return ret
        elif process_name == 'patch-model':
            self.patch_model(
                data.path,
                **kwargs
            )
            return dict(status='OK')
        else:
            raise ValueError('')

    async def coco_image(
        self,
        fBytesIO: io.BytesIO,
        fname_org: str,
        **kwargs
    ):
        img_pil = Image.open(fBytesIO)
        img_np = np.asarray(img_pil)
        # print(img_np.shape) # (h, w, 3)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        # print(img_np.shape) # height, width, chanel

        images = [coco_formatter.create_image(
            id = 0,
            width = img_np.shape[1],
            height = img_np.shape[0],
            file_name = fname_org
        )]

        annotations = func.detection_image(
            self.session,
            img_np,
            self.imsize,
            convert_catid=self.cvt_catid,
            th_conf = kwargs['th_conf'],
            th_nms = kwargs['th_nms'],
            categories = kwargs['categories']
        )
        
        return dict(
            images = images,
            annotations = annotations
        )
