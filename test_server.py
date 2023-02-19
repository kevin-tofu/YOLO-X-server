
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


def test_coco():
    with open(f"{path_data}/{name_image}", "rb") as _file:
        res = testclient.post("/coco_image?test=1", files={"file": (f"_{name_image}", _file, "image/jpeg")})
    assert res.status_code == 200
    assert type(res.json()) == dict

    with open(f"{path_data}/{name_video}", "rb") as _file:
        res = testclient.post("/coco_video/?test=1", files={"file": (f"_{name_video}", _file, "video/mp4")})
    assert res.status_code == 200
    assert type(res.json()) == dict

if __name__ == "__main__":
    
    test_read_main()
    test_coco()