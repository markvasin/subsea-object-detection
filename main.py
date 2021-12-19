import torch
import uvicorn
from decouple import config
from fastapi import FastAPI
from pydantic import BaseModel

path = config('path')
# TODO: For local testing, comment out the above lines and uncomment the below line.
# path = 'test'

app = FastAPI()


def get_yolov5(weight):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=f'./model/{weight}', device='cpu')
    model.conf = 0.25  # NMS confidence threshold
    model.iou = 0.45  # NMS IoU threshold
    return model


model = get_yolov5(weight='breezy.pt')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/" + path)
def read_root():
    return {"Hello": "World"}


class Payload(BaseModel):
    url: str
    image_id: str


category = {
    "pipe": 1,
    "corner": 2,
    "flange": 3,
    "anode": 4
}
img_size = 640


@app.post("/" + path + "/predict")
def predict(payload: Payload):
    # TODO: Deep learning & Machine learning code here. For example:
    # img_bytes = requests.get(payload.url).content
    # img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), cv2.IMREAD_COLOR)

    # Example response must be like the below structure. If there is no bounding
    # boxes in the image, please return an empty list of "bbox_list".

    results = model(payload.url, size=img_size)
    det_results = results.pandas().xyxy[0].to_dict('records')
    outputs = []
    for res in det_results:
        out = {
            'category_id': category[res['name']],  # res['class'],
            'bbox': {
                "x": res['xmin'],  # top left (pixel)
                "y": res['ymin'],  # top left (pixel)
                "w": res['xmax'] - res['xmin'],  # width (pixel)
                "h": res['ymax'] - res['ymin']  # height (pixel)
            },
            "score": res['confidence']
        }
        outputs.append(out)

    response = {
        "image_id": payload.image_id,
        "bbox_list": outputs
    }
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
