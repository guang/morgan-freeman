from flask import (
    Flask,
    flash,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from settings import snapi_logger
# from datetime import datetime
from util import (
    s3_to_local,
    data_to_s3,
    allowed_file,
)
from os.path import basename
# import json
import uuid
# import requests


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('SNAPI_CONFIGS_PATH')
    return app


app = create_app()
db = SQLAlchemy(app)

CORS(app)

from models import *    # NOQA


@app.route('/')
def index():
    return render_template('index.html', name='guang')


@app.route('/api', methods=['GET'])
def api_versions():
    return 'v1'


@app.route('/upload_wav', methods=['GET', 'POST'])
def upload_wav():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            session_id = str(uuid.uuid4())
            # saved_path = '/home/dev/' + session_id + '.wav'
            # file.save(saved_path)
            # snapi_logger.info("file saved to {}".format(saved_path))
            s3_key = 'user_data/' + session_id + '.wav'
            data_to_s3(file, s3_key)
            snapi_logger.info("file saved to {}".format(s3_key))
            return redirect(url_for('check_status', session_id=session_id))
    return render_template('upload_wav.html')


@app.route('/check_status/<session_id>', methods=['GET', 'POST'])
def check_status(session_id):
    return "hey cutie :) ur session_id is {}".format(session_id)

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
    data, errors = inference_schema.load(json_data)   # NOQA

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
    # from infer import do_convert
    # do_convert(
    #     args,
    #     logdir1,
    #     logdir2
    # )

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
