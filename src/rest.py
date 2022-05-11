import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep

import rq
from flask import Flask, request
from flask_executor import Executor
from redis import Redis

from edie.api import ApiClient
from edie.config import Config
from edie.evaluator import Edie
from edie.model import Dictionary
from edie.service import EvaluationService
from metrics.base import MetadataMetric, EntryMetric


def create_app(edie: Edie, metadata_evaluators: [MetadataMetric], entry_evaluators: [EntryMetric], config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.evaluation_service = EvaluationService(edie)
    app.executor = ThreadPoolExecutor(10)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/evaluations", methods=['POST', 'GET'])
    def evaluate():
        evaluation_id: uuid.UUID = uuid.uuid4()
        # job = app.task_queue.enqueue(app.evaluation_service.evaluate, evaluation_id)
        app.executor.submit(app.evaluation_service.evaluate, evaluation_id)
        return {'message': 'Accepted', 'evaluation_id': evaluation_id}, 202

    return app
