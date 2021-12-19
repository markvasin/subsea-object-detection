import io
import json
import os
from pathlib import Path

import pandas as pd


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_data_path():
    return os.path.join(get_project_root(), 'data')


def get_image_path(data_split):
    return os.path.join(get_data_path(), data_split)


def get_annotation_path():
    return os.path.join(get_data_path(), 'annotations')


def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_damage_cls_dict(file_name):
    cls_file = os.path.join(get_data_path(), file_name)
    cls_df = pd.read_csv(cls_file)
    cls_dict = {row['class']: row['id'] for i, row in cls_df.iterrows()}
    return cls_dict


def read_json(file_path):
    with open(file_path, 'rt', encoding='UTF-8') as file:
        json_file = json.load(file)
    return json_file


def write_json(json_data, file_path):
    with io.open(file_path, mode='w', encoding='utf8') as fout:
        json.dump(json_data, fout, indent=2)
