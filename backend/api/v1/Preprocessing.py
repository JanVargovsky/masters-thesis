from flask_restplus import Namespace, Resource, fields

from infrastructure.DatasetUtils import get_dataset, save_dataset
from infrastructure.Preprocessing import train_test_split, modify
from infrastructure.PreprocessingConfiguration import save_configuration, get_configurations

api = Namespace('preprocessing')

dataset_split = api.model('PreprocessingDatasetSplit', {
    'dataset': fields.String(required=True, description='Dataset name'),
    'ratio': fields.Float(required=True, description='Split ratio', min=0.001, max=0.999),
    'shuffle': fields.Boolean(default=True, description='Shuffle dataset'),
    'trainDataset': fields.String(required=True, description='Train dataset name'),
    'testDataset': fields.String(required=True, description='Test dataset name')
})


@api.route('/split')
class Split(Resource):
    @api.expect(dataset_split, validate=True)
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


dataset_modify_normalize_range = api.model('PreprocessingDatasetNormalizeColumnRange', {
    'min': fields.Float(default=0),
    'max': fields.Float(default=1)
})

dataset_modify_column = api.model('PreprocessingDatasetModifyColumn', {
    'name': fields.String(required=True),

    'remove': fields.Boolean(default=False, description='Remove'),

    'normalize': fields.Boolean(default=False, description='Normalize'),
    'normalizeRange': fields.Nested(dataset_modify_normalize_range),

    'na': fields.Boolean(default=False, description='Replace NA values'),
    'naMethod': fields.String(desription='Replacement method of NA values',
                              enum=['zero', 'average', 'common', 'custom']),
    'naCustomValue': fields.String(description='Custom replacement value of NA values'),

    'encode': fields.Boolean(default=False, description='Encode categorical'),
    'encodeMethod': fields.String(description='Encoding method', enum=['label', 'oneHot'])
})

dataset_modify = api.model('PreprocessingDatasetModify', {
    'newDatasetName': fields.String(),
    'configurationName': fields.String(),
    'columns': fields.Nested(dataset_modify_column, as_list=True, required=True)
})


@api.route('/modify/<string:dataset>')
class Modify(Resource):
    def get(self, dataset):
        df = get_dataset(dataset)
        columns = []
        for column in df:
            series = df[column]
            columns.append({
                'name': column,
                'type': series.dtype.name,
                'hasNA': bool(series.isnull().any())
            })

        return {
            'columns': columns
        }

    @api.expect(dataset_modify, validate=True)
    def put(self, dataset):
        df = get_dataset(dataset)
        columns = api.payload['columns']

        if 'newDatasetName' in api.payload and api.payload['newDatasetName']:
            dataset_name = api.payload['newDatasetName']
            modify(df, columns)
            save_dataset(df, dataset_name)

        if 'configurationName' in api.payload and api.payload['configurationName']:
            configuration_name = api.payload['configurationName']
            save_configuration(columns, configuration_name)

        return None, 200


@api.route('/configurations')
class Configurations(Resource):
    def get(self):
        return list(get_configurations())
