from flask import Flask
from flask_cors import CORS
import requests
from api.v1 import api_v1

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_v1, url_prefix='/api/v1')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def frontend_proxy(path):
    # TODO: return requested file for production
    return requests.get('http://localhost:8080/{}'.format(path)).content


if __name__ == '__main__':
    app.run()
