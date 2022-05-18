import uuid
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request

from edie.service import EvaluationService
from edie.vocabulary import Vocabulary


def create_app():
    app = Flask(__name__)
    app.evaluation_service = EvaluationService()
    app.executor = ThreadPoolExecutor(10)

    @app.route("/")
    def home():
        return "<p>This is Edie</p>"

    @app.route("/evaluations", methods=['POST', 'GET'])
    def evaluate():
        if request.method == 'POST':
            evaluation_id: uuid.UUID = uuid.uuid4()
            app.executor.submit(app.evaluation_service.evaluate, evaluation_id, request.json['endpoint'], request.json['api-key'])
            return {'message': 'Accepted', 'evaluation_id': evaluation_id}, 202
        elif request.method == 'GET':
            return {'evaluations': app.evaluation_service.get_evaluations()}, 200

    @app.route("/evaluations/<evaluation_id>", methods=['GET'])
    def get_evaluation(evaluation_id):
        if request.method == 'GET':
            evaluation = app.evaluation_service.get_evaluation(evaluation_id)
            if evaluation is None:
                return "Evaluation Not Available", 404
            elif evaluation['status'] == Vocabulary.EvaluationStatus.IN_PROGRESS:
                return evaluation, 202
            elif evaluation['status'] == Vocabulary.EvaluationStatus.FAILED:
                return evaluation, 500
            else:
                return evaluation, 200

    @app.route("/evaluations/<evaluation_id>/<dictionary_id>", methods=['GET'])
    def get_dictionary_evaluation(evaluation_id, dictionary_id):
        if request.method == 'GET':
            dict_evaluation = app.evaluation_service.get_dictionary_evaluation(evaluation_id, dictionary_id)
            if dict_evaluation is None:
                return "Dictionary evaluation not available", 404
            else:
                return dict_evaluation, 200
    return app
