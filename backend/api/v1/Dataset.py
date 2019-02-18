import numpy as np
from flask import request
from flask_restplus import Namespace, Resource

from infrastructure import datasets_path
from infrastructure.DatasetUtils import get_dataset, get_dataset_rows, delete_dataset
from infrastructure.PlotUtils import plot_histogram, plot_to_base64
from infrastructure.Preprocessing import modify
from infrastructure.PreprocessingConfiguration import load_configuration, get_configurations
from infrastructure.StatisticsCache import store, try_load

api = Namespace('dataset')


class DatasetBase(Resource):
    def get(self, dataset, rows):
        df = get_dataset(dataset, rows, True)
        columns = df.columns.values.tolist()
        column_types = list(map(lambda t: t.name, df.dtypes.values))
        data_preview = df.values.tolist()
        return {
            'columns': columns,
            'columnTypes': column_types,
            'rows': data_preview
        }


@api.route('/<string:dataset>')
class Dataset(DatasetBase):
    def get(self, dataset):
        return super().get(dataset, None)

    def delete(self, dataset):
        delete_dataset(dataset)
        return None, 204

    def post(self, dataset):
        file = request.files['dataset']
        file.save(datasets_path + dataset)
        return None, 201


@api.route('/<string:dataset>/<int:rows>')
class DatasetWithLimitedRows(DatasetBase):
    def get(self, dataset, rows):
        return super().get(dataset, rows)


@api.route('/rows/<string:dataset>')
class DatasetRows(Resource):
    def get(self, dataset):
        return {
            'rows': get_dataset_rows(dataset)
        }


@api.route('/statistics/<string:dataset>')
@api.route('/statistics/<string:dataset>/<string:configuration>')
class DatasetStatistics(Resource):
    def get(self, dataset, configuration=None):
        result = try_load(dataset, configuration)
        if result:
            return result

        df = get_dataset(dataset)
        if configuration:
            loaded_configuration = load_configuration(dataset, configuration)
            modify(df, loaded_configuration)

        columns = []
        for column_name in df:
            series = df[column_name]
            describe = series.describe()

            is_numeric = np.issubdtype(series.dtype, np.number)
            if is_numeric:
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

            plot_histogram(series, column_name, is_numeric)
            histogram = plot_to_base64()

            columns.append({
                "name": column_name,
                "type": series.dtype.name,
                "numeric": is_numeric,
                "descriptiveStatistics": descriptive_statistics,
                "histogramType": "base64",
                "histogram": histogram
            })

        result = {
            "columns": columns
        }
        store(dataset, configuration, result)

        return result


@api.route('/configurations/<string:dataset>')
class DatasetConfigurations(Resource):
    def get(self, dataset):
        return list(get_configurations(dataset))
