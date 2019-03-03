from tensorflow import keras
from sklearn.model_selection import KFold


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

    def fit(self, **kwargs):
        return self.model.fit(**kwargs)

    def score(self, **kwargs):
        metrics = self.model.evaluate(**kwargs)
        return dict(zip(self.model.metrics_names, metrics))

    def predict_classes(self, x, **kwargs):
        return self.model.predict_classes(x, **kwargs)
