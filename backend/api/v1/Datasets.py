from flask_restplus import Namespace, Resource, fields, marshal_with
from infrastructure.DatasetUtils import get_datasets

api = Namespace('datasets')

resource_fields = {
    'name': fields.String,
    'type': fields.String,
    'size': fields.Integer,
    'createdAt': fields.DateTime('iso8601'),
    'lastModifiedAt': fields.DateTime('iso8601'),
}


@api.route('')
class Datasets(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return list(get_datasets())
