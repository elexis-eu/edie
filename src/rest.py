import uuid
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request

from edie.service import EvaluationService


def create_app():
    app = Flask(__name__)
    app.evaluation_service = EvaluationService()
    app.executor = ThreadPoolExecutor(10)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/evaluations", methods=['POST', 'GET'])
    def evaluate():

        if request.method == 'POST':
            evaluation_id: uuid.UUID = uuid.uuid4()
            app.executor.submit(app.evaluation_service.evaluate, evaluation_id, request.json['endpoint'], request.json['api-key'])
            return {'message': 'Accepted', 'evaluation_id': evaluation_id}, 202

    @app.route("/evaluations/<evaluation_id>", methods=['GET'])
    def get_evaluation():
        pass

    @app.route("/evaluations/<evaluation_id>/<dictionary_id>", methods=['GET'])
    def get_dictionary_evaluation():
        pass

    return app
