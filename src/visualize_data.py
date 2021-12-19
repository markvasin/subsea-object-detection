import os

import fiftyone as fo

from utils.project_utils import get_data_path

image_path = os.path.join(get_data_path(), 'dataset_v1.0', 'images')
label_path = os.path.join(get_data_path(), 'dataset_v1.0', 'train.json')
dataset_name = 'arv'

dataset_type = fo.types.COCODetectionDataset
dataset = fo.Dataset.from_dir(dataset_type=dataset_type,
                              data_path=image_path,
                              labels_path=label_path,
                              name=dataset_name,
                              label_types=['detections'],
                              include_id=True,
                              label_field="")

session = fo.launch_app(dataset)
session.wait()
