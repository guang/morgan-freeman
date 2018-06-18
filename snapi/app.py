from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from settings import snapi_logger
# from datetime import datetime
from util import s3_to_local
# import json
from os.path import basename
# import uuid
# import requests


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('SNAPI_CONFIGS_PATH')
    return app


app = create_app()
db = SQLAlchemy(app)

CORS(app)

from models import (
    inference_schema,
)


@app.route('/')
def index():
    return "hay guyz"


@app.route('/api', methods=['GET'])
def api_versions():
    return 'v1'


# @app.route('/api/v1/user_voice', methods=['POST'])
# def new_user_voice():
#     # params
#     json_data = request.get_json(force=True)
#     if not json_data:
#         return jsonify({'message': 'No input data provided'}), 400
#
#     # Validate and deserialize input
#     data, errors = user_voice_schema.load(json_data)
#     if errors:
#         return jsonify(errors), 422
#
#     data['created_at'] = datetime.now()
#     user_voice = UserVoice(**data)
#     db.session.add(user_voice)
#     db.session.commit()
#
#     return jsonify(
#         {
#             "message": "",
#             "session_id": base_metric.id,
#         }
#     )


@app.route('/api/v1/infer/<session_id>', methods=['POST'])
def new_inference(session_id):
    # params
    json_data = request.get_json(force=True)
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and deserialize input
    data, errors = inference_schema.load(json_data)

    # pull user voice data
    # override if given input #TODO: remove me
    s3_loc = data['user_voice_location']
    if not s3_loc:
        raise Exception("Sorry not implemented yet, please give user_voice_location")
        # get_s3_location_by_session_id(session_id=, table=UserVoice.__tablename__)

    tmp_loc = '{path}/{base}'.format(path='/tmp/', base=basename(s3_loc))
    snapi_logger.info("storing input file temporarily at '{}'".format(tmp_loc))

    s3_to_local(s3_loc, tmp_loc)

    # run inference
    # remember to put this in PYTHONPATH
    from infer import do_convert
    do_convert(
        args,
        logdir1,
        logdir2
    )

    # push converted voice data
    # import pdb; pdb.set_trace()
    if errors:
        return jsonify(errors), 422

    return jsonify(
        {
            "message": "Created new inference.",
            "converted_voice_location": 'TODO',
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
