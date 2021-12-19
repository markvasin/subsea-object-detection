import json
import logging
from pathlib import Path

import datasetinsights.constants as const
from PIL import Image
from datasetinsights.datasets.transformers.base import DatasetTransformer
from datasetinsights.datasets.unity_perception import (
    AnnotationDefinitions,
    Captures,
)

logger = logging.getLogger(__name__)


class COCOInstancesTransformer(DatasetTransformer, format="COCO-Instances"):
    """Convert Synthetic dataset to COCO format.
    This transformer convert Synthetic dataset into annotations in instance
    format (e.g. instances_train2017.json, instances_val2017.json)
    Note: We assume "valid images" in the COCO dataset must contain at least one
    bounding box annotation. Therefore, all images that contain no bounding
    boxes will be dropped. Instance segmentation are considered optional
    in the converted dataset as some synthetic dataset might be generated
    without it.
    Args:
        data_root (str): root directory of the dataset
    """

    # The annotation_definition.name is not a reliable way to know the type
    # of annotation definition. This will be improved once the perception
    # package introduced the annotation definition type in the future.
    BBOX_NAME = r"^(?:2[dD]\s)?bounding\sbox$"
    INSTANCE_SEGMENTATION_NAME = r"^instance\ssegmentation$"

    def __init__(self, data_root):
        self._data_root = Path(data_root)

        # self.image_id = 0
        self.ann_id = 0

        ann_def = AnnotationDefinitions(
            data_root, version=const.DEFAULT_PERCEPTION_VERSION
        )
        self._bbox_def = ann_def.find_by_name(self.BBOX_NAME)

        captures = Captures(
            data_root=data_root, version=const.DEFAULT_PERCEPTION_VERSION
        )
        self._bbox_captures = captures.filter(self._bbox_def["id"])

    def execute(self, output, **kwargs):
        """Execute COCO Transformer
        Args:
            output (str): the output directory where converted dataset will
              be stored.
        """
        # self._copy_images(output)
        self._process_instances(output)

    # def _copy_images(self, output):
    #     image_to_folder = Path(output) / "images"
    #     image_to_folder.mkdir(parents=True, exist_ok=True)
    #     for _, row in self._bbox_captures.iterrows():
    #         image_from = self._data_root / row["filename"]
    #         if not image_from.exists():
    #             continue
    #         capture_id = uuid_to_int(row["id"])
    #         image_to = image_to_folder / f"camera_{capture_id}.png"
    #         shutil.copy(str(image_from), str(image_to))

    def _process_instances(self, output):
        output = Path(output) / "annotations"
        output.mkdir(parents=True, exist_ok=True)
        instances = {
            "info": {"description": "COCO compatible Synthetic Dataset"},
            "licences": [{"url": "", "id": 1, "name": "default"}],
            "images": self._images(),
            "annotations": self._annotations(),
            "categories": self._categories(),
        }
        output_file = output / "instances.json"
        with open(output_file, "w") as out:
            json.dump(instances, out)

    def _images(self):
        images = []
        for id, row in self._bbox_captures.iterrows():
            image_file = self._data_root / row["filename"]
            if not image_file.exists():
                continue
            with Image.open(image_file) as im:
                width, height = im.size

            record = {
                "file_name": row["filename"].split('/')[-1],  # f"camera_{capture_id}.png",
                "height": height,
                "width": width,
                "id": id,
            }
            images.append(record)

        return images

    def _annotations(self):
        annotations = []
        for id, row in self._bbox_captures.iterrows():
            image_id = id
            for ann in row["annotation.values"]:
                x = ann["x"]
                y = ann["y"]
                w = ann["width"]
                h = ann["height"]
                area = float(w) * float(h)
                record = {
                    # "segmentation": [],  # TODO: parse instance segmentation map
                    "area": area,
                    "iscrowd": 0,
                    "image_id": image_id,
                    "bbox": [x, y, w, h],
                    "category_id": ann["label_id"],
                    "id": self.ann_id,
                }
                self.ann_id += 1
                annotations.append(record)

        return annotations

    def _categories(self):
        categories = []
        for r in self._bbox_def["spec"]:
            record = {
                "id": r["label_id"],
                "name": r["label_name"],
                "supercategory": "default",
            }
            categories.append(record)

        return categories


data_root = '/Users/vasin/Projects/subsea-object-detection/data/394a3980-29e6-4dc4-a9b4-b84a2d30c97b'
output = '/Users/vasin/Projects/subsea-object-detection/data/synthetic_v1.0'
converter = COCOInstancesTransformer(data_root)
converter.execute(output)