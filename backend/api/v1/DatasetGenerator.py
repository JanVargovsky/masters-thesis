from abc import abstractmethod

import numpy as np
import pandas as pd
from flask_restplus import Namespace, Resource, fields
from sklearn.datasets import make_classification, make_blobs, make_circles, make_moons, make_gaussian_quantiles, \
    make_s_curve, make_swiss_roll

from infrastructure.DatasetUtils import save_dataset
from infrastructure.PlotUtils import plot_generated_dataset, plot_to_base64

api = Namespace('dataset-generator')


class DatasetGeneratorBase(Resource):
    def _get_random_state(self):
        return api.payload['randomState'] if 'randomState' in api.payload else np.random.randint(0, 10000)

    @abstractmethod
    def _generate(self, random_state):
        raise NotImplementedError

    # preview
    def post(self):
        random_state = self._get_random_state()
        x, y = self._generate(random_state)

        plot_generated_dataset(x, y)
        plot = plot_to_base64()

        return {
            'randomState': random_state,
            'plot': plot
        }

    # create
    def put(self):
        name = api.payload['datasetName']
        random_state = self._get_random_state()
        x, y = self._generate(random_state)
        df = pd.DataFrame(x)
        df['class'] = y

        save_dataset(df, name)

        return None, 201


classification_model = api.model('GenerateClassificationDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'features': fields.Integer(required=True),
    'classes': fields.Integer(required=True),
    'informative': fields.Integer(required=True)
})


@api.route('/classification')
@api.expect(classification_model, validate=True)
class Classification(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        features = api.payload['features']
        classes = api.payload['classes']
        informative = api.payload['informative']

        return make_classification(
            random_state=random_state,
            n_samples=rows,
            n_features=features,
            n_classes=classes,
            n_informative=informative,
            n_redundant=0,
            n_repeated=0,
            n_clusters_per_class=1)


blobs_model = api.model('GenerateBlobsDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'features': fields.Integer(required=True),
    'classes': fields.Integer(required=True),
    'clusterStd': fields.Float(required=True)
})


@api.route('/blobs')
@api.expect(blobs_model, validate=True)
class Blobs(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        features = api.payload['features']
        classes = api.payload['classes']
        cluster_std = api.payload['clusterStd']

        return make_blobs(
            random_state=random_state,
            n_samples=rows,
            n_features=features,
            centers=classes,
            center_box=(0, 1),
            cluster_std=cluster_std)


circles_model = api.model('GenerateCirclesDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'noise': fields.Float(required=True)
})


@api.route('/circles')
@api.expect(circles_model, validate=True)
class Circles(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        noise = api.payload['noise']

        return make_circles(
            random_state=random_state,
            n_samples=rows,
            noise=noise)


moons_model = api.model('GenerateMoonsDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'noise': fields.Float(required=True)
})


@api.route('/moons')
@api.expect(moons_model, validate=True)
class Classification(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        noise = api.payload['noise']

        return make_moons(
            random_state=random_state,
            n_samples=rows,
            noise=noise)


gaussian_quantiles_model = api.model('GenerateGaussianQuantilesDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'features': fields.Integer(required=True),
    'classes': fields.Integer(required=True)
})


@api.route('/gaussian-quantiles')
@api.expect(gaussian_quantiles_model, validate=True)
class GaussianQuantiles(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        features = api.payload['features']
        classes = api.payload['classes']

        return make_gaussian_quantiles(
            random_state=random_state,
            n_samples=rows,
            n_features=features,
            n_classes=classes,
            cov=1.0)


s_curve_model = api.model('GenerateSCurveDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'noise': fields.Float(required=True),
    'classes': fields.Integer()
})


@api.route('/s-curve')
@api.expect(s_curve_model, validate=True)
class SCurve(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        noise = api.payload['noise']

        x, y = make_s_curve(
            random_state=random_state,
            n_samples=rows,
            noise=noise)

        if 'classes' in api.payload:
            classes = api.payload['classes']
            if classes is not None and classes > 0:
                categories = pd.cut(y, classes)
                y = categories.codes

        return x, y


swiss_roll_model = api.model('GenerateSwissRollDataset', {
    'datasetName': fields.String(),
    'randomState': fields.Integer(),
    'rows': fields.Integer(required=True),
    'noise': fields.Float(required=True),
    'classes': fields.Integer()
})


@api.route('/swiss-roll')
@api.expect(swiss_roll_model, validate=True)
class SwissRoll(DatasetGeneratorBase):
    def _generate(self, random_state):
        rows = api.payload['rows']
        noise = api.payload['noise']

        x, y = make_swiss_roll(
            random_state=random_state,
            n_samples=rows,
            noise=noise)

        if 'classes' in api.payload:
            classes = api.payload['classes']
            if classes is not None and classes > 0:
                categories = pd.cut(y, classes)
                y = categories.codes

        return x, y
