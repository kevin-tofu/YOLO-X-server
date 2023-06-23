from typing import Optional, Callable, Union
import os

import cv2
import numpy as np
from controllers.utils import *

import onnxruntime
from onnxruntime.capi.onnxruntime_inference_collection import InferenceSession
import coco_formatter


def x1y1x2y2_x1y1wh(bbox: Union[list, np.ndarray]):
    return [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]


def detection_image(
    session: InferenceSession, 
    image: np.ndarray, 
    input_shape: tuple, 
    image_id: int=0,
    ann_id_base: int=0,
    convert_catid: Callable[[int], int]=lambda a: a,
    th_conf: float=0.5,
    th_nms: float=0.5,
    categories: Optional[list[int]] = None
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
        nms_thr=th_nms, 
        score_thr=th_conf
    )
    anns = []

    if dets is not None:
        # final_boxes, final_scores, final_cls_inds = dets[:, :4], dets[:, 4], dets[:, 5]
        idloop = 0
        for det in dets:
            det_list = det.tolist()
            # id_class = det_list[5]
            id_class = convert_catid(int(det_list[5]))
            # print(categories, id_class)
            if not categories is None:
                if not id_class in categories:
                    continue
            
            bbox, score = det_list[:4], det_list[4]
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
                    id = idloop + ann_id_base, 
                    image_id = image_id, 
                    category_id = id_class, 
                    area = bbox[2]*bbox[3], 
                    bbox = bbox, 
                    score=score
                )
            )
            idloop += 1
    
    # ret = dict(
    #     annotations=anns
    # )
    # print(ret)
    return anns



def detection_video(
    session: InferenceSession, 
    fpath: str, 
    input_shape: tuple, 
    fpath_dst: Optional[str]=None, 
    image_id: int=0,
    ann_id_base: int=0,
    convert_catid: Callable[[int], int]=lambda a: a,
    th_conf: float=0.5,
    th_nms: float=0.5,
    categories: Optional[list[int]] = None
):

    cap = cv2.VideoCapture(fpath)
    k = cap.isOpened()
    if k == False:
        cap.open(fpath)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # if kwargs['process'] == 'detection-drawing':
    # # if kwargs['process'] == 'detection-drawing' or kwargs['process'] == 'detection-drawing-bg':
    #     fpath_ex = os.path.splitext(fpath_dst)[-1]
    #     if fpath_ex == ".mp4" or fpath_ex == ".MP4":
    #         fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #     writer = cv2.VideoWriter(fpath_dst, fmt, fps, (width, height))

    imgid = image_id
    annids = ann_id_base
    ann_image_list = list()
    ann_annotation_list = list()

    while(1):

        ret, image = cap.read()
        if ret == False:
            break

        coco_image = coco_formatter.create_image(
            id = imgid,
            width = image.shape[1],
            height = image.shape[0],
            file_name = os.path.basename(fpath)
        )
        coco_annotations = detection_image(
            session,
            image,
            input_shape,
            image_id = imgid,
            ann_id_base = annids,
            convert_catid = convert_catid,
            th_conf=th_conf,
            th_nms=th_nms,
            categories=categories
        )

        ann_image_list.append(coco_image)
        imgid += 1
        if len(coco_annotations) > 0:
            ann_annotation_list.extend(coco_annotations)
            annids = coco_annotations[-1]['id'] + 1

        # if kwargs['process'] == 'detection-drawing':
        #     image_visualize = visualize.draw_bbox2img(np.asarray(image_rgb), ann_bbox_list_temp, th=kwargs["th_conf"])
        #     image_visualize = cv2.cvtColor(image_visualize, cv2.COLOR_RGB2BGR)
        #     writer.write(image_visualize)

    cap.release()
    # if kwargs['process'] == 'detection-drawing':
    #     writer.release()
    if False:
        pass
    else:
        ret = dict(
            images = ann_image_list,
            annotations = ann_annotation_list
        )
        # print(ret)
        return ret