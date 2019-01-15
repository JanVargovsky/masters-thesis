from flask_restplus import Namespace, Resource
from infrastructure.DatasetUtils import get_dataset, get_dataset_rows

api = Namespace('dataset')


@api.route('/<string:dataset>')
@api.route('/<string:dataset>/<int:rows>')
class Dataset(Resource):
    def get(self, dataset, rows=None):
        df = get_dataset(dataset, rows)
        columns = df.columns.values.tolist()
        column_types = list(map(lambda t: t.name, df.dtypes.values))
        data_preview = df.values.tolist()
        return {
            'columns': columns,
            'columnTypes': column_types,
            'rows': data_preview
        }


@api.route('/rows/<string:dataset>')
class DatasetRows(Resource):
    def get(self, dataset):
        return {
            'rows': get_dataset_rows(dataset)
        }
