from infrastructure import preprocessing_configuration_path
import json
import glob
import os


def _get_filename(name):
    return f"{preprocessing_configuration_path}{name}.json"


def save_configuration(data, name):
    # TODO: prune
    filename = _get_filename(name)
    with open(filename, 'x') as f:
        json.dump(data, f, indent=2)


def load_configuration(name):
    filename = _get_filename(name)
    with open(filename, 'r') as f:
        return json.load(f)


def get_configurations():
    for glob_path in glob.glob(preprocessing_configuration_path + '*.json'):
        filename = os.path.basename(glob_path)
        name = os.path.splitext(filename)[0]
        yield name
