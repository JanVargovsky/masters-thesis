import pandas as pd
import requests
from flask_restplus import Namespace, Resource, fields
from sklearn.datasets import fetch_openml

from infrastructure.DatasetUtils import save_dataset

api = Namespace('dataset-import')

openml_dataset = api.model('OpenMLDataset', {
    'datasetName': fields.String(required=True)
})


@api.route('/openml/<int:id>')
class OpenML(Resource):
    def get(self, id):
        response = requests.get('https://www.openml.org/api/v1/json/data/{}'.format(id))
        return response.json()

    @api.expect(openml_dataset, validate=True)
    def post(self, id):
        dataset_name = api.payload['datasetName']
        data = fetch_openml(data_id=id)

        x = data.data
        if data.details['format'] == 'Sparse_ARFF':
            x = x.toarray()
        y = data.target
        columns = data.feature_names
        y_name = data.details['default_target_attribute']

        df = pd.DataFrame(x, columns=columns)
        df[y_name] = y

        save_dataset(df, dataset_name)
        return None, 201
