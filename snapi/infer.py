# -*- coding: utf-8 -*-
# /usr/bin/python2
''' Based on andabi/deep-voice-conversion/convert.py
'''


from __future__ import print_function

import argparse
import numpy as np
import datetime
import tensorflow as tf
import librosa

from models import Net2
from audio import (
    spec2wav,
    inv_preemphasis,
    db2amp,
    denormalize_db,
    write_wav,
)
from hparam import hparam as hp
from data_load import Net2DataFlow
from tensorpack.predict.base import OfflinePredictor
from tensorpack.predict.config import PredictConfig
from tensorpack.tfutils.sessinit import SaverRestore
from tensorpack.tfutils.sessinit import ChainInit


def convert(predictor, df):
    # TODO need to fix reading in with duration
    pred_spec, y_spec, ppgs = predictor(next(df().get_data()))

    # Denormalizatoin
    pred_spec = denormalize_db(pred_spec, hp.default.max_db, hp.default.min_db)
    y_spec = denormalize_db(y_spec, hp.default.max_db, hp.default.min_db)

    # Db to amp
    pred_spec = db2amp(pred_spec)
    y_spec = db2amp(y_spec)

    # Emphasize the magnitude
    pred_spec = np.power(pred_spec, hp.convert.emphasis_magnitude)
    y_spec = np.power(y_spec, hp.convert.emphasis_magnitude)

    # Spectrogram to waveform
    audio = np.array(map(lambda spec: spec2wav(spec.T, hp.default.n_fft, hp.default.win_length, hp.default.hop_length,
                                               hp.default.n_iter), pred_spec))
    y_audio = np.array(map(lambda spec: spec2wav(spec.T, hp.default.n_fft, hp.default.win_length, hp.default.hop_length,
                                                 hp.default.n_iter), y_spec))

    # Apply inverse pre-emphasis
    audio = inv_preemphasis(audio, coeff=hp.default.preemphasis)
    y_audio = inv_preemphasis(y_audio, coeff=hp.default.preemphasis)

    if hp.convert.one_full_wav:
        # Concatenate to a wav
        y_audio = np.reshape(y_audio, (1, y_audio.size), order='C')
        audio = np.reshape(audio, (1, audio.size), order='C')

    return audio, y_audio, ppgs


def get_eval_input_names():
    return ['x_mfccs', 'y_spec', 'y_mel']


def get_eval_output_names():
    return ['pred_spec', 'y_spec', 'ppgs']


def do_convert(logdir1, logdir2, input_path, output_path):
    # Load graph
    model = Net2()
    model.actual_duration = librosa.core.get_duration(filename=input_path, sr=hp.default.sr)

    # TODO isolate out logdirs, uhh and how to pre-dl from s3?

    assert len(input_path) > 0, "must be non-empty input path"

    df = Net2DataFlow(data_path=input_path, batch_size=1)

    ckpt1 = tf.train.latest_checkpoint(logdir1)
    ckpt2 = tf.train.latest_checkpoint(logdir2)
    session_inits = []
    session_inits.append(SaverRestore(ckpt2))
    session_inits.append(SaverRestore(ckpt1, ignore=['global_step']))
    pred_conf = PredictConfig(
        model=model,
        input_names=get_eval_input_names(),
        output_names=get_eval_output_names(),
        session_init=ChainInit(session_inits))
    predictor = OfflinePredictor(pred_conf)

    audio, y_audio, ppgs = convert(predictor, df)

    write_wav(audio[0], hp.default.sr, output_path)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('logdir1', type=str, help='full path to logdir of train1')
    parser.add_argument('logdir2', type=str, help='full path to logdir of train2')
    parser.add_argument('-input_path', help='absolute path to input .wav file')
    parser.add_argument('-output_path', help='absolute path to output .wav file')
    parser.add_argument('-ckpt', help='checkpoint to load model.')
    # TODO: make these into mandatory positional arguments
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    args = get_arguments()

    s = datetime.datetime.now()

    do_convert(logdir1=args.logdir1, logdir2=args.logdir2, input_path=args.input_path, output_path=args.output_path)

    e = datetime.datetime.now()
    diff = e - s
    print("Done. elapsed time:{}s".format(diff.seconds))
