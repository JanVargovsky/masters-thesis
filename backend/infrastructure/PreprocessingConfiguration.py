import glob
import json
import os
from pathlib import Path

from infrastructure import preprocessing_configuration_path


def _get_filename(dataset, configuration):
    return "{}{}/{}.json".format(preprocessing_configuration_path, dataset, configuration)


def save_configuration(dataset, name, data):
    # TODO: prune
    filename = _get_filename(dataset, name)
    Path(preprocessing_configuration_path + dataset).mkdir(parents=True, exist_ok=True)
    with open(filename, 'x') as f:
        json.dump(data, f, indent=2)


def load_configuration(dataset, name):
    filename = _get_filename(dataset, name)
    with open(filename, 'r') as f:
        return json.load(f)


def get_configurations(dataset):
    for glob_path in glob.glob(preprocessing_configuration_path + dataset + '/*.json'):
        filename = os.path.basename(glob_path)
        name = os.path.splitext(filename)[0]
        yield name


def delete_configuration(dataset, name):
    filename = _get_filename(dataset, name)
    os.remove(filename)
