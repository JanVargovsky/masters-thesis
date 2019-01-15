import os
import glob
from pathlib import Path
import platform
from datetime import datetime
import pandas as pd

data_path = 'data/'
datasets_path = data_path + 'datasets/'


def get_datasets():
    supported_extensions = ['csv', 'txt']
    for extension in supported_extensions:
        for glob_path in glob.glob(datasets_path + '*.' + extension):
            path = Path(glob_path)
            stat = os.stat(glob_path)
            created_at = _get_creation_timestamp(stat)
            last_modified_at = stat.st_mtime
            yield {
                'name': path.name,
                'type': extension,
                'size': stat.st_size,
                'createdAt': datetime.fromtimestamp(created_at),
                'lastModifiedAt': datetime.fromtimestamp(last_modified_at)
            }


def get_dataset(name, nrows=None):
    return pd.read_csv(datasets_path + name, sep=None, nrows=nrows, engine='python')


def save_dataset(dataset, name):
    dataset.to_csv(datasets_path + name, index=False)


def get_dataset_rows(name):
    with open(datasets_path + name) as f:
        return sum(1 for _ in f) - 1


def _get_creation_timestamp(stat):
    if platform.system() == 'Windows':
        return stat.st_ctime
    else:
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
