import glob
import os
import platform
from datetime import datetime
from pathlib import Path

import pandas as pd

from infrastructure import datasets_path
from infrastructure.FileUtils import get_extension

supported_types = {
    'csv': ['csv'],
    'text': ['txt'],
    'excel': ['xlsx', 'xlsm'],
    'pickle': ['pickle'],
    'feather': ['feather'],
    'parquet': ['parquet'],
    'hdf': ['hdf', 'hdf5', 'h5']
}


def get_datasets():
    for file_type, supported_extensions in supported_types.items():
        for extension in supported_extensions:
            for glob_path in glob.glob(datasets_path + '*.' + extension):
                path = Path(glob_path)
                stat = os.stat(glob_path)
                created_at = _get_creation_timestamp(stat)
                last_modified_at = stat.st_mtime
                yield {
                    'name': path.name,
                    'type': file_type,
                    'size': stat.st_size,
                    'createdAt': datetime.fromtimestamp(created_at),
                    'lastModifiedAt': datetime.fromtimestamp(last_modified_at)
                }


def get_dataset(name, nrows=None, fillna=False):
    file_type = _get_type(name)
    path = datasets_path + name
    if file_type == 'csv':
        df = pd.read_csv(path, sep=None, nrows=nrows, engine='python')
    elif file_type == 'excel':
        df = pd.read_excel(path, nrows=nrows)
    elif file_type == 'pickle':
        df = pd.read_pickle(path)[:nrows]
    elif file_type == 'feather':
        df = pd.read_feather(path)[:nrows]
    elif file_type == 'parquet':
        df = pd.read_parquet(path)[:nrows]
    elif file_type == 'hdf':
        df = pd.read_hdf(path)[:nrows]
    else:
        raise Exception("Unknown dataset type")

    if fillna:
        df = df.where(pd.notnull(df), None)
    return df


def save_dataset(dataset, name):
    file_type = _get_type(name)
    path = datasets_path + name
    if file_type == 'csv':
        dataset.to_csv(path, index=False)
    elif file_type == 'excel':
        dataset.to_excel(path, index=False)
    elif file_type == 'pickle':
        dataset.to_pickle(path)
    elif file_type == 'feather':
        dataset.reset_index(drop=True, inplace=True)
        dataset.to_feather(path)
    elif file_type == 'parquet':
        dataset.to_parquet(path)
    elif file_type == 'hdf':
        dataset.to_hdf(path, 'df')
    else:
        raise Exception("Unknown dataset type")


def delete_dataset(name):
    path = datasets_path + name
    os.remove(path)


def get_dataset_rows(name):
    file_type = _get_type(name)
    path = datasets_path + name
    if file_type == 'csv':
        with open(path) as f:
            return sum(1 for _ in f) - 1
    else:
        df = get_dataset(name)
        return len(df)


def _get_creation_timestamp(stat):
    if platform.system() == 'Windows':
        return stat.st_ctime
    else:
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


def _get_type(name):
    extension = get_extension(name)
    for file_type, supported_extensions in supported_types.items():
        if extension in supported_extensions:
            return file_type
    return 'unknown'
