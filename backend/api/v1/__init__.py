from importlib import import_module
from pkgutil import iter_modules

from flask import Blueprint
from flask_restplus import Api

api_v1 = Blueprint('api/v1', __name__)
api = Api(api_v1, doc='/docs')

for _, modname, _ in iter_modules(path=__path__, prefix=__name__ + '.'):
    module = import_module(modname)
    namespace = getattr(module, 'api', None)
    if namespace:
        print(f"adding namespace {namespace.name}")
        api.add_namespace(namespace)
