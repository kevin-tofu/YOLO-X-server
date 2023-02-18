# YOLO-X Server

## WebAPI for YOLO-series model  

## API

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
    }

    if (timeout !== undefined){  
      config_post["timeout"] = timeout
    }

    if (c_params.value !== undefined){
      config_post["params"] = Object.assign(
        {}, 
        ...c_params.value.map( 
          function(data_loop) {
            return {[data_loop.label]: data_loop.value}
          })
      )
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
