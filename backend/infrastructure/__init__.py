from pathlib import Path

data_path = 'data/'
datasets_path = data_path + 'datasets/'
preprocessing_configuration_path = data_path + 'preprocessing/'


def _create_directories(*args):
    for path in args:
        Path(path).mkdir(parents=True, exist_ok=True)


_create_directories(datasets_path, preprocessing_configuration_path)