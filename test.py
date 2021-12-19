import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model/breezy.pt', device='cpu')
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45
# Images
img_size = 640
img = 'https://github.com/Rovula/hackathon-fastapi/blob/master/doc/20201107122805838.png?raw=true'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img, size=img_size)

# Results
results.show()  # or .show(), .save(), .crop(), .pandas(), etc.