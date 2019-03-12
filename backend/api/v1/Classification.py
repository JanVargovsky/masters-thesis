from flask_restplus import Namespace, Resource, fields
from tensorflow import keras
from sklearn.utils import shuffle
from collections import OrderedDict

from infrastructure.Classification import ClassificationModel
from infrastructure.DatasetUtils import get_dataset
from infrastructure.PlotUtils import plot_history_accuracy, plot_history_loss, plot_to_base64, \
    plot_classification_predictions
from infrastructure.PreprocessingConfiguration import load_configuration
from infrastructure.Preprocessing import modify

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
class ClassificationTestRun(Resource):
    @api.expect(classification_test_run, validate=True)
    def post(self):
        dataset = api.payload['dataset']
        df = get_dataset(dataset)

        if 'configuration' in api.payload:
            configuration_name = api.payload['configuration']
            configuration = load_configuration(dataset, configuration_name)
            modify(df, configuration)

        df = shuffle(df, random_state=42)

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

        plots = OrderedDict()

        plot_history_accuracy(history)
        plots['accuracy'] = plot_to_base64()
        plot_history_loss(history)
        plots['loss'] = plot_to_base64()

        plot_classification_predictions(data_y, predicts, orientation='vertical', stacked=False)
        plots['predictions'] = plot_to_base64()

        plot_classification_predictions(data_y, predicts, orientation='vertical', stacked=True)
        plots['predictions2'] = plot_to_base64()

        plot_classification_predictions(data_y, predicts, orientation='horizontal', stacked=False)
        plots['predictions3'] = plot_to_base64()

        plot_classification_predictions(data_y, predicts, orientation='horizontal', stacked=True)
        plots['predictions4'] = plot_to_base64()

        return {
            'score': score,
            'plots': plots
        }
