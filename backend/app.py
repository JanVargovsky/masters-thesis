import matplotlib.pyplot as plt
from flask import Flask
from flask_cors import CORS

from api.v1 import api_v1

app = Flask(__name__, static_url_path='', static_folder='frontend')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_v1, url_prefix='/api/v1')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

plt.style.use('ggplot')


@app.route('/')
def default():
    return app.send_static_file('index.html')


# import requests
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def frontend_proxy(path):
#     return requests.get('http://localhost:8080/{}'.format(path)).content


if __name__ == '__main__':
    app.run()
