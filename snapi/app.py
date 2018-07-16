from flask import (
    Flask,
    # flash,
    request,
    render_template,
    redirect,
)
from flask_cors import CORS
from settings import snapi_logger
from util import (
    s3_to_local,
    data_to_s3,
    allowed_file,
)
import uuid
# TODO: OOooff this is janky lets remove
import subprocess
import wave
import contextlib


# TODO put this into utils
LOG_DIR_1 = "/s3_data/model/current/train1"
LOG_DIR_2 = "/s3_data/model/current/{voice_profile_id}/train2"
CURRENT_VOICE_PROFILES = [
    {'name': 'Judy Greer', 'id': 1},
    {'name': 'James Earl Jones', 'id': 2},
    {'name': 'Samuel Jackson', 'id': 4},
]
MAX_DURATION = 30


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('SNAPI_CONFIGS_PATH')
    return app


app = create_app()
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api', methods=['GET'])
def api_versions():
    return 'v1'


@app.route('/upload_wav', methods=['GET', 'POST'])
def upload_wav():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            session_id = str(uuid.uuid4())
            s3_key = 'user_data/' + session_id + '.wav'
            data_to_s3(file, s3_key)
            snapi_logger.info("file saved to {}".format(s3_key))

            error = new_inference(
                session_id=session_id,
                voice_profile_id=int(request.form.get('chosen_vprofile')),
            )
            if not error:
                return render_template('play.html', session_id=session_id)
            else:
                # flash(error)
                return error
                return render_template('upload_wav.html', voice_profiles=CURRENT_VOICE_PROFILES)

    return render_template('upload_wav.html', voice_profiles=CURRENT_VOICE_PROFILES)


def new_inference(session_id, voice_profile_id):

    # pull user voice data and save it to tmp local
    # override if given input #TODO: remove me
    s3_key = 'user_data/' + session_id + '.wav'

    # TODO: clean up names right now to avoid creating new dirs
    raw_tmp_loc = '{prefix}/raw-{local_path}'.format(prefix='/tmp', local_path=s3_key.replace('/', '-'))
    tmp_loc = '{prefix}/{local_path}'.format(prefix='/tmp', local_path=s3_key.replace('/', '-'))
    tmp_out_loc = '{prefix}/{local_path}'.format(prefix='/tmp', local_path='out'+s3_key.replace('/', '-'))
    snapi_logger.info("storing input file temporarily at '{}'".format(raw_tmp_loc))

    s3_to_local(s3_key, raw_tmp_loc)
    # -- validate duration not too long --
    with contextlib.closing(wave.open(raw_tmp_loc, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    snapi_logger.info("Detected duration {}".format(duration))
    if duration > MAX_DURATION:
        return 'Voice clip length is too long'

    # --- resample from 44100 to 16000, oouuff this is pretty flimsy ---
    cmd_to_run_resample = """sox {RAW} -r 16000 {INPUT}""".format(
        RAW=raw_tmp_loc,
        INPUT=tmp_loc,
    )
    snapi_logger.info("running resampling, with command '{}'".format(cmd_to_run_resample))
    subprocess.check_call(cmd_to_run_resample, shell=True)

    # run inference
    # remember to put this in PYTHONPATH
    snapi_logger.info("running inference, with logdir2 {}".format(LOG_DIR_2.format(voice_profile_id=voice_profile_id)))
    cmd_to_run_inference = """cd $HOME/morgan-freeman/snapi && python infer.py {LOG_DIR_1} {LOG_DIR_2} -input_path {INPUT_PATH} -output_path {OUTPUT_PATH}""".format(
        LOG_DIR_1=LOG_DIR_1,
        LOG_DIR_2=LOG_DIR_2.format(voice_profile_id=voice_profile_id),
        INPUT_PATH=tmp_loc,
        OUTPUT_PATH=tmp_out_loc,
    )

    snapi_logger.info("running inference, with command '{}'".format(cmd_to_run_inference))
    subprocess.check_call(cmd_to_run_inference, shell=True)

    # push converted voice data
    s3_out_key = 'inference/' + session_id + '.wav'
    snapi_logger.info("finished running inference, uploading to {}".format(s3_out_key))
    with open(tmp_out_loc, 'rb') as temp_wav:
        data_to_s3(temp_wav, s3_out_key, bucket_name='bwhoyouwant2-be-data-public')


@app.route('/play/<session_id>', methods=['GET'])
def play(session_id):
    return render_template('play.html', session_id=session_id)


@app.route('/version', methods=['GET'])
def git_versions():
    return 'not implemented'


@app.route('/healthz', methods=['GET'])
def get_health():
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
