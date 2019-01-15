from flask_restplus import Namespace, Resource, fields
import tensorflow as tf
from tensorflow import keras
from infrastructure.DatasetUtils import get_dataset

api = Namespace('model')


@api.route('/validate/<string:training>/<string:testing>')
class Validate(Resource):
    def get(self, training, testing):
        train = get_dataset(training, 5)
        test = get_dataset(testing, 5)

        result = {
            'length': len(train.columns) == len(test.columns),
            'columns': False,
            'types': False,
        }

        if result['length']:
            result['columns'] = bool((train.columns == test.columns).all())
            result['types'] = bool((train.dtypes.asobject == test.dtypes.asobject).all())

        return result


simple_classification_experiment = api.model('SimpleClassificationExperiment', {
    'name': fields.String(required=True, description='Experiment name'),
    'trainingDataset': fields.String(required=True, description='Training dataset'),
    'testingDataset': fields.String(required=True, description='Testing dataset'),
    'labelColumnName': fields.String(required=True, description='Label')
})


@api.route('/classification/simple')
class ClassificationSimple(Resource):
    @api.expect(simple_classification_experiment, validate=True)
    def post(self):
        experiment_name = api.payload['name']
        train_dataset_name = api.payload['trainingDataset']
        test_dataset_name = api.payload['testingDataset']
        label_column_name = api.payload['labelColumnName']

        train = get_dataset(train_dataset_name)
        test = get_dataset(test_dataset_name)

        train_x, train_y_raw = self._split_xy(train, label_column_name)
        test_x, test_y_raw = self._split_xy(test, label_column_name)

        train_y, classes = train_y_raw.factorize(sort=True)
        test_y, _ = test_y_raw.factorize(sort=True)

        # prepare model
        model = keras.Sequential([
            keras.layers.Dense(16, activation=tf.nn.relu, input_shape=train_x.shape[1:]),
            keras.layers.Dense(len(classes), activation=tf.nn.softmax)
        ])

        model.summary()

        # compile model
        model.compile(optimizer=tf.train.AdamOptimizer(),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        # train
        model.fit(train_x, train_y, epochs=15, validation_split=0.1)

        # test
        test_loss, test_acc = model.evaluate(test_x, test_y)

        keras.models.save_model(model, f'data/models/{experiment_name}.h5py')

        return {
            'testLoss': test_loss,
            'testAccuracy': test_acc
        }

    @staticmethod
    def _split_xy(data, y_name):
        return data.drop(y_name, axis=1), data[y_name]
