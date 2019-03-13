import json
import os
import shutil
from pathlib import Path

from tensorflow import keras

from infrastructure import classification_models_path


class ClassificationModel:
    def __init__(self, input_dim, output_dim, layers):
        model = keras.Sequential()

        model.add(keras.layers.Dense(layers[0], input_dim=input_dim, activation='relu'))
        for layer in layers[1:]:
            model.add(keras.layers.Dense(layer, activation='relu'))
        model.add(keras.layers.Dense(output_dim, activation='softmax'))

        model.compile(optimizer=keras.optimizers.Adam(),
                      loss=keras.losses.sparse_categorical_crossentropy,
                      metrics=['accuracy'])

        self.model = model

    def __del__(self):
        del self.model

    def fit(self, **kwargs):
        return self.model.fit(**kwargs)

    def score(self, **kwargs):
        metrics = self.model.evaluate(**kwargs)
        return dict(zip(self.model.metrics_names, metrics))

    def predict_classes(self, x, **kwargs):
        return self.model.predict_classes(x, **kwargs)

    def save(self, name):
        self.model.save(name)

    @staticmethod
    def load(name):
        instance = ClassificationModel.__new__(ClassificationModel)
        instance.model = keras.models.load_model(name)
        return instance


def save_model(model, name, metadata):
    path = classification_models_path + name
    Path(path).mkdir(parents=True, exist_ok=True)

    model.save(path + '/model.h5')
    with open(path + '/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)


def load_model(name):
    path = classification_models_path + name + '/model.h5'
    return ClassificationModel.load(path)


def load_model_metadata(name):
    path = classification_models_path + name + '/metadata.json'
    with open(path, 'r') as f:
        return json.load(f)


def get_model_names():
    return next(os.walk(classification_models_path))[1]


def remove_model(name):
    shutil.rmtree(classification_models_path + name)
