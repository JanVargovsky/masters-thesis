from pathlib import Path

data_path = 'data/'
datasets_path = data_path + 'datasets/'
preprocessing_configuration_path = data_path + 'preprocessing/'
statistics_cache_path = data_path + 'statistics-cache/'
models_path = data_path + 'models/'
classification_models_path = models_path + 'classification/'


def _create_directories(*args):
    for path in args:
        Path(path).mkdir(parents=True, exist_ok=True)


_create_directories(datasets_path,
                    preprocessing_configuration_path,
                    statistics_cache_path,
                    models_path,
                    classification_models_path)
