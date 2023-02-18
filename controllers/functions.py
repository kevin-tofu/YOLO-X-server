from typing import Optional, Callable, Union, List
import os

import cv2
import numpy as np
from controllers.utils import *

import onnxruntime
from onnxruntime.capi.onnxruntime_inference_collection import InferenceSession
import coco_formatter


def x1y1x2y2_x1y1wh(bbox: Union[List, np.ndarray]):
    return [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]


def coco_image(
    session: InferenceSession, 
    image: np.ndarray, 
    input_shape: tuple, 
    image_id: int=0,
    ann_id_base: int=0,
    convert_catid: Callable[[int], int]=lambda a: a
):
    """
    """
    # args = make_parser().parse_args()

    # input_shape = tuple(map(int, args.input_shape.split(',')))
    # origin_img = cv2.imread(args.image_path)
    img, ratio = preproc(image, input_shape)

    # session = onnxruntime.InferenceSession(args.model)

    ort_inputs = {session.get_inputs()[0].name: img[None, :, :, :]}
    output = session.run(None, ort_inputs)
    predictions = demo_postprocess(output[0], input_shape)[0]

    boxes = predictions[:, :4]
    scores = predictions[:, 4:5] * predictions[:, 5:]

    boxes_xyxy = np.ones_like(boxes)
    boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2]/2.
    boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3]/2.
    boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2]/2.
    boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3]/2.
    boxes_xyxy /= ratio
    dets = multiclass_nms(
        boxes_xyxy, 
        scores, 
        nms_thr=0.45, 
        score_thr=0.1
    )
    anns = []

    if dets is not None:
        final_boxes, final_scores, final_cls_inds = dets[:, :4], dets[:, 4], dets[:, 5]
        for loop, det in enumerate(dets):
            det_list = det.tolist()
            bbox, score, id_class = det_list[:4], det_list[4], det_list[5]
            # print('id_class', id_class)
            bbox = x1y1x2y2_x1y1wh(bbox)
            anns.append(
                # dict(
                #     id = loop + ann_id_base, 
                #     image_id = image_id, 
                #     category_id = id_class, 
                #     # segmentation = , 
                #     area = box[2]*box[3], 
                #     bbox = box, 
                #     iscrowd = 0
                # )
                coco_formatter.create_annotation_bbox(
                    id = loop + ann_id_base, 
                    image_id = image_id, 
                    category_id = convert_catid(int(id_class)), 
                    area = bbox[2]*bbox[3], 
                    bbox = bbox, 
                )
            )
    
    # ret = dict(
    #     annotations=anns
    # )
    # print(ret)
    return anns