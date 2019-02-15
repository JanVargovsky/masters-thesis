import json

from infrastructure import statistics_cache_path


def _get_filename(dataset, configuration):
    filename = f"{statistics_cache_path}{dataset}"
    if configuration:
        filename += configuration
    return filename + ".json"


def store(dataset, configuration, result):
    filename = _get_filename(dataset, configuration)
    with open(filename, 'w') as f:
        json.dump(result, f)


def try_load(dataset, configuration):
    try:
        filename = _get_filename(dataset, configuration)
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
