from flask_restplus import Namespace, Resource
from infrastructure.DatasetUtils import get_dataset, get_dataset_rows
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

api = Namespace('dataset')


@api.route('/<string:dataset>')
@api.route('/<string:dataset>/<int:rows>')
class Dataset(Resource):
    def get(self, dataset, rows=None):
        df = get_dataset(dataset, rows, True)
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


@api.route('/statistics/<string:dataset>')
class DatasetStatistics(Resource):
    def get(self, dataset):
        df = get_dataset(dataset)
        columns = []
        for column_name in df:
            series = df[column_name]
            describe = series.describe()

            numeric = np.issubdtype(series.dtype, np.number)
            if numeric:
                descriptive_statistics = {
                    "count": int(describe["count"]),
                    "mean": describe["mean"],
                    "std": describe["std"],
                    "min": describe["min"],
                    "p25": describe['25%'],
                    "p50": describe["50%"],
                    "p75": describe["75%"],
                    "max": describe["max"]
                }
            else:
                descriptive_statistics = {
                    "count": int(describe["count"]),
                    "unique": int(describe["unique"])
                }

            image = io.BytesIO()
            plt.title(f"{column_name} histogram")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.hist(series.dropna(), bins='auto' if numeric else None)
            plt.savefig(image, format='png', dpi=150, transparent=False)
            plt.clf()
            histogram = base64.b64encode(image.getvalue()).decode()

            columns.append({
                "name": column_name,
                "type": series.dtype.name,
                "numeric": numeric,
                "descriptiveStatistics": descriptive_statistics,
                "histogramType": "base64",
                "histogram": histogram
            })

        return {
            "columns": columns
        }
