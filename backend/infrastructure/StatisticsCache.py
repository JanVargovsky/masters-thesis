from infrastructure import statistics_cache_path
import json


def store(dataset, result):
    with open(f"{statistics_cache_path}{dataset}.json", 'w') as f:
        json.dump(result, f)


def try_load(dataset):
    try:
        with open(f"{statistics_cache_path}{dataset}.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
