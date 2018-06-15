from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_cors import CORS
from settings import snapi_logger
import json
import os
import uuid
import requests


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('SNAPI_CONFIGS_PATH')
    return app


app = create_app()
db = SQLAlchemy(app)

CORS(app)

from models import *        # NOQA


@app.route('/')
def index():
    return "hay guyz"


@app.route('/api', methods=['GET'])
def api_versions():
    return 'v1'


@app.route('/api/v1/infer/<session_id>', methods=['POST'])
def new_inference(session_id):
    # params
    json_data = request.get_json(force=True)
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and deserialize input
    data, errors = inference_schema.load(json_data)

    # import pdb; pdb.set_trace()
    if errors:
        return jsonify(errors), 422

    return jsonify(
        {
            "message": "Created new snapi.",
            "metric_id": metric.id,
            "base_metric_id": base_metric.id,
        }
    )


@app.route('/version', methods=['GET'])
def git_versions():
    return 'not implemented'


@app.route('/healthz', methods=['GET'])
def get_health():
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
