from flask_restplus import Namespace, Resource, fields
from infrastructure.DatasetUtils import get_dataset, save_dataset
from infrastructure.Preprocessing import train_test_split
from pathlib import Path

api = Namespace('preprocessing')

dataset_train_test_split = api.model('DatasetTrainTestSplit', {
    'dataset': fields.String(required=True, description='Dataset name'),
    'ratio': fields.Float(required=True, description='Split ratio', min=0.001, max=0.999),
    'shuffle': fields.Boolean(default=True, description='Shuffle dataset'),
    'trainDataset': fields.String(required=True, description='Train dataset name'),
    'testDataset': fields.String(required=True, description='Test dataset name')
})


@api.route('/split')
class Split(Resource):
    @api.expect(dataset_train_test_split, validate=True)
    def put(self):
        dataset_name = api.payload['dataset']
        ratio = api.payload['ratio']
        shuffle = api.payload['shuffle']
        train_dataset_name = api.payload['trainDataset']
        test_dataset_name = api.payload['testDataset']

        dataset = get_dataset(dataset_name)
        train, test = train_test_split(dataset, ratio, shuffle)

        save_dataset(train, train_dataset_name)
        save_dataset(test, test_dataset_name)

        return None, 200

    def _create_dataset_name(self, name, type):
        path = Path(name)
        path.stem
