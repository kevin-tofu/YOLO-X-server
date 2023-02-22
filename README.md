# YOLO-X Server

 This web server provides WEB-API for object detection model.  
Although the name of this repository is "YOLO-X server", general object detection model can be used on this server if the output of models is having common format. Because of any types of YOLO(Object Detection model) can be used, the repository is named to 'YOLO-X (any type of yolo or object detection) Server'.  

## Use YOLOX as Example

 Lets use YOLOX as an example <https://github.com/Megvii-BaseDetection/YOLOX>.  
Since this repository has onnx-conversion function and converted model weight itself<https://yolox.readthedocs.io/en/latest/demo/onnx_readme.html>, the model is easy to be introduced.  

### How to build

```bash
docker build ./ --build-arg URL_MODEL=https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_m.onnx -t yolo-server
```

### How to run

```bash
docker run -it -d --name yolox -p 5500:80 yolo-server
```

## WebAPI for YOLO-series model  

| Route | Method | Query / Body | Description |
| --- | --- | --- | --- |
| /coco_image | POST | - | Post an image(.mp4 ) to get bboxes. The Data is described in COCO format. |
| /coco_video | POST | - | Post a video(.mp4 ) to get bboxes. The Data is described in COCO format. |
| /categories | GET | - | GET categories of detected objects with id, name and super-category . |

## Environment variables

| Variable | required | Description |
| --- | --- | --- |
| APP_PORT | false | The port to which the application listens to, default is set to 80 |
| PATH_MODEL | false | Path name for model. |

## How to Run

```python
python server.py --port 3333
```

## Code Example using axios

```javascript
  let isConverted = ref(false)
  let isConverting = ref(false)
  let progress_value = ref(0)
  let res = reactive([])
  let max_progress_value = 100

  const handleFilePost = () => {

    isConverting.value = true

    var fd = new FormData();
    fd.append('file', file_selected.value)
    const url_post = `${url_host}/${api_post}/`

    const config_post = { 
      headers:{ 
        'Content-Type': 'multipart/form-data', 
      },
      onUploadProgress: (event) => {
        progress_value.value = Math.round( max_progress_value * event.loaded / event.total)
      },
      params: {
        th_conf: 0.5,
        th_nms: 0.5
      },
      timeout: 60000
    }

    axios.post(url_post, fd, config_post).then(res_post => {

      res.value = {
        data: res_post.data
      }
      // console.log(res.value)
      isConverted.value = true

    }).catch((e) => {
      console.log(e)
    }).finally(() => {
      isConverting.value = false
    })
  }

  return {
    handleFilePost,
    isConverted,
    isConverting,
    progress_value,
    file_selected,
    res
  }

```
