from flask_restplus import Namespace, Resource, fields
from tensorflow import keras
from sklearn.utils import shuffle

from infrastructure.Classification import ClassificationModel
from infrastructure.DatasetUtils import get_dataset
from infrastructure.PlotUtils import plot_history_accuracy, plot_history_loss, plot_to_base64
from infrastructure.PreprocessingConfiguration import load_configuration
from infrastructure.Preprocessing import modify

api = Namespace('classification')

classification_test_run = api.model('ClassificationTestRun', {
    'dataset': fields.String(required=True, description='Dataset'),
    'labelColumn': fields.String(required=True, description='Name of the label column'),
    'configuration': fields.String(description='Configuration name')
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
        epochs = 200
        layers = [32, 32]
        validation_split = 0.3

        model = ClassificationModel(input_dim, output_dim, layers)

        history = model.fit(x=data_x, y=data_y, epochs=epochs, verbose=0, validation_split=validation_split)

        keras.backend.clear_session()

        plot_history_accuracy(history)
        plot_accuracy = plot_to_base64()
        plot_history_loss(history)
        plot_loss = plot_to_base64()

        return {
            'plotAccuracy': plot_accuracy,
            'plotLoss': plot_loss
        }
