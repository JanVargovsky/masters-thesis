from collections import OrderedDict

from flask_restplus import Namespace, Resource, fields
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle
from tensorflow import keras

from infrastructure.Classification import ClassificationModel, save_model, load_model, load_model_metadata, \
    get_model_names, remove_model
from infrastructure.DatasetUtils import get_dataset
from infrastructure.PlotUtils import plot_history_accuracy, plot_history_loss, plot_to_base64, \
    plot_classification_predictions, plot_cross_validation
from infrastructure.Preprocessing import modify
from infrastructure.PreprocessingConfiguration import load_configuration

api = Namespace('classification')

classification_test_run = api.model('ClassificationTestRun', {
    'dataset': fields.String(required=True, description='Dataset'),
    'labelColumn': fields.String(required=True, description='Name of the label column'),
    'configuration': fields.String(description='Configuration name'),
    'epochs': fields.Integer(required=True, min=1, description='Number of epochs to train the model'),
    'layers': fields.List(fields.Integer, required=True, description="Number of neurons in each dense layer"),
    'validationSplit': fields.Float(min=0, max=1, description="Number of neurons in each dense layer")
})


@api.route('/test-run')
class TestRun(Resource):
    @api.expect(classification_test_run, validate=True)
    def post(self):
        dataset = api.payload['dataset']
        df = get_dataset(dataset)

        if 'configuration' in api.payload:
            configuration_name = api.payload['configuration']
            configuration = load_configuration(dataset, configuration_name)
            modify(df, configuration)

        df = shuffle(df)

        label = api.payload['labelColumn']
        data_x = df.drop(label, axis=1)
        data_y = df[label]

        input_dim = data_x.columns.size
        output_dim = data_y.unique().size
        epochs = api.payload['epochs']
        layers = api.payload['layers']
        for layer in layers:
            if layer <= 0:
                return "Invalid layer", 400

        validation_split = api.payload['validationSplit'] if 'validationSplit' in api.payload else 0

        keras.backend.clear_session()
        model = ClassificationModel(input_dim, output_dim, layers)

        history = model.fit(x=data_x, y=data_y, epochs=epochs, verbose=2, validation_split=validation_split)
        predicts = model.predict_classes(data_x)
        score = float((data_y == predicts).sum() / predicts.size)
        conf_matrix = confusion_matrix(data_y, predicts)

        plots = OrderedDict()

        plot_history_accuracy(history)
        plots['accuracy'] = plot_to_base64()
        plot_history_loss(history)
        plots['loss'] = plot_to_base64()

        plot_classification_predictions(data_y, predicts, orientation='vertical', stacked=False)
        plots['predictions'] = plot_to_base64()

        return {
            'score': score,
            'plots': plots,
            'confusionMatrix': conf_matrix.tolist()
        }


cross_validation_classification_model = api.model('CrossValidationClassificationModel', {
    'dataset': fields.String(required=True, description='Dataset'),
    'labelColumn': fields.String(required=True, description='Name of the label column'),
    'configuration': fields.String(description='Configuration name'),
    'epochs': fields.Integer(required=True, min=1, description='Number of epochs to train the model'),
    'layers': fields.List(fields.Integer, required=True, description="Number of neurons in each dense layer"),
    'kfolds': fields.Integer(min=3, max=10, description="Number of k-folds")
})


@api.route('/cross-validation')
class CrossValidation(Resource):
    @api.expect(cross_validation_classification_model, validate=True)
    def post(self):
        dataset = api.payload['dataset']
        df = get_dataset(dataset)

        if 'configuration' in api.payload:
            configuration_name = api.payload['configuration']
            configuration = load_configuration(dataset, configuration_name)
            modify(df, configuration)

        label = api.payload['labelColumn']
        data_x = df.drop(label, axis=1)
        data_y = df[label]

        input_dim = data_x.columns.size
        output_dim = data_y.unique().size
        epochs = api.payload['epochs']
        layers = api.payload['layers']
        for layer in layers:
            if layer <= 0:
                return "Invalid layer", 400

        train_scores = []
        test_scores = []
        kfolds = api.payload['kfolds'] if 'kfolds' in api.payload else 10
        kf = StratifiedKFold(n_splits=kfolds, shuffle=True)
        for train_indices, test_indices in kf.split(data_x, data_y):
            train_x, train_y = data_x.iloc[train_indices], data_y.iloc[train_indices]
            test_x, test_y = data_x.iloc[test_indices], data_y.iloc[test_indices]

            keras.backend.clear_session()
            model = ClassificationModel(input_dim, output_dim, layers)

            model.fit(x=train_x, y=train_y.values, epochs=epochs, verbose=2)

            predicts = model.predict_classes(train_x)
            score = float((train_y == predicts).sum() / predicts.size)
            train_scores.append(score)

            predicts = model.predict_classes(test_x)
            score = float((test_y == predicts).sum() / predicts.size)
            test_scores.append(score)

        plots = OrderedDict()

        plot_cross_validation(train_scores, test_scores, plot_type='bar')
        plots['crossValidation'] = plot_to_base64()
        plot_cross_validation(train_scores, test_scores, plot_type='plot')
        plots['crossValidation2'] = plot_to_base64()

        return {
            'trainScores': train_scores,
            'testScores': test_scores,
            'plots': plots,
        }


create_classification_model = api.model('CreateClassificationModel', {
    'dataset': fields.String(required=True, description='Dataset'),
    'labelColumn': fields.String(required=True, description='Name of the label column'),
    'configuration': fields.String(description='Configuration name'),
    'epochs': fields.Integer(required=True, min=1, description='Number of epochs to train the model'),
    'layers': fields.List(fields.Integer, required=True, description="Number of neurons in each dense layer"),
    'validationSplit': fields.Float(min=0, max=1, description="Number of neurons in each dense layer")
})


@api.route('/<string:name>')
class Model(Resource):
    @api.expect(create_classification_model, validate=True)
    def post(self, name):
        dataset = api.payload['dataset']
        df = get_dataset(dataset)

        if 'configuration' in api.payload:
            configuration_name = api.payload['configuration']
            configuration = load_configuration(dataset, configuration_name)
            modify(df, configuration)

        df = shuffle(df)

        label = api.payload['labelColumn']
        data_x = df.drop(label, axis=1)
        data_y = df[label]

        input_dim = data_x.columns.size
        output_dim = data_y.unique().size
        epochs = api.payload['epochs']
        layers = api.payload['layers']
        for layer in layers:
            if layer <= 0:
                return "Invalid layer", 400

        validation_split = api.payload['validationSplit'] if 'validationSplit' in api.payload else 0

        keras.backend.clear_session()
        model = ClassificationModel(input_dim, output_dim, layers)

        history = model.fit(x=data_x, y=data_y, epochs=epochs, verbose=2, validation_split=validation_split)
        predicts = model.predict_classes(data_x)
        score = float((data_y == predicts).sum() / predicts.size)
        conf_matrix = confusion_matrix(data_y, predicts)

        plots = OrderedDict()

        plot_history_accuracy(history)
        plots['accuracy'] = plot_to_base64()
        plot_history_loss(history)
        plots['loss'] = plot_to_base64()

        plot_classification_predictions(data_y, predicts, orientation='vertical', stacked=False)
        plots['predictions'] = plot_to_base64()

        metadata = {
            'dataset': dataset,
            'configuration': configuration_name if 'configuration' in api.payload else None,
            'label': label,
            'inputDimension': input_dim,
            'outputDimension': output_dim,
            'score': score,
            'epochs': epochs,
            'layers': layers,
            'plots': plots,
            'confusionMatrix': conf_matrix.tolist()
        }
        save_model(model, name, metadata)

        return {
            'score': score,
            'plots': plots,
            'confusionMatrix': conf_matrix.tolist()
        }

    def get(self, name):
        return load_model_metadata(name)

    def delete(self, name):
        remove_model(name)
        return None, 204


@api.route('/<string:name>/predict/<string:dataset>')
class Predict(Resource):
    def get(self, name, dataset):
        model = load_model(name)
        metadata = load_model_metadata(name)
        df = get_dataset(dataset)

        # TODO: make it optional
        if metadata['configuration']:
            configuration = load_configuration(metadata['dataset'], metadata['configuration'])
            modify(df, configuration)

        label = metadata['label']
        data_x = df.drop(label, axis=1)
        data_y = df[label]

        predicts = model.predict_classes(data_x)
        score = float((data_y == predicts).sum() / predicts.size)
        conf_matrix = confusion_matrix(data_y, predicts)

        plots = OrderedDict()

        plot_classification_predictions(data_y, predicts, orientation='vertical', stacked=False)
        plots['predictions'] = plot_to_base64()

        return {
            'score': score,
            'plots': plots,
            'confusionMatrix': conf_matrix.tolist()
        }


@api.route('')
class List(Resource):
    def get(self):
        return get_model_names()
