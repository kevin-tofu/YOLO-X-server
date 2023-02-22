
from fastapi.testclient import TestClient
# from main import app
from server import app

import config


path_data = config.PATH_DATA
name_video = 'test_video.mp4'
name_image = 'test_image.jpg'
name_image_wrong = 'test_image.jp'

testclient = TestClient(app)

def test_read_main():
    res = testclient.get('')
    assert res.status_code == 200
    assert type(res.json()) == dict


def test_image():
    params0  = dict(
        test = 1,
        th_conf = 0.12,
        th_nms = 0.3
    )
    with open(f"{path_data}/{name_image}", "rb") as _file:
        res = testclient.post(
            "/coco_image", 
            files={"file": (f"_{name_image}", _file, "image/jpeg")},
            params=params0
        )
    assert res.status_code == 200
    assert type(res.json()) == dict

    params1  = dict(
        test = 1,
        filter_categories = [1, 2]
    )
    with open(f"{path_data}/{name_image}", "rb") as _file:
        res = testclient.post(
            "/coco_image", 
            params=params1,
            files={"file": (f"_{name_image}", _file, "image/jpeg")}
        )
    assert res.status_code == 200
    assert type(res.json()) == dict

def test_video():
    params2  = dict(
        test = 1,
        filter_categories = [1, 2],
        th_conf = 0.12,
        th_nms = 0.3
    )
    with open(f"{path_data}/{name_video}", "rb") as _file:
        res = testclient.post(
            "/coco_video/?test=1", 
            params=params2,
            files={"file": (f"_{name_video}", _file, "video/mp4")}
        )
    assert res.status_code == 200
    assert type(res.json()) == dict

    

if __name__ == "__main__":
    
    test_read_main()
    
    test_image()
    
    test_video()