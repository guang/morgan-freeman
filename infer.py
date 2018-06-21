# -*- coding: utf-8 -*-
# /usr/bin/python2
''' Based on andabi/deep-voice-conversion/convert.py
'''


from __future__ import print_function

import argparse
import numpy as np
import datetime
import tensorflow as tf

from deep_voice_conversion.models import Net2
from deep_voice_conversion.audio import (
    spec2wav,
    inv_preemphasis,
    db2amp,
    denormalize_db,
    write_wav,
)
from deep_voice_conversion.hparam import hparam as hp
from deep_voice_conversion.data_load import Net2DataFlow
from tensorpack.predict.base import OfflinePredictor
from tensorpack.predict.config import PredictConfig
from tensorpack.tfutils.sessinit import SaverRestore
from tensorpack.tfutils.sessinit import ChainInit
from tensorpack.callbacks.base import Callback


def convert(predictor, df):
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


def do_convert(args, logdir1, logdir2):
    # Load graph
    model = Net2()
    # TODO auto detect duration, dont chop

    # TODO isolate out logdirs, uhh and how to pre-dl from s3?

    # TODO make this into an input
    args.input_path = hp.convert.data_path
    assert len(args.input_path) > 0, "must be non-empty input path"
    df = Net2DataFlow(data_path=args.input_path, batch_size=1)

    ckpt1 = tf.train.latest_checkpoint(logdir1)
    ckpt2 = '{}/{}'.format(logdir2, args.ckpt) if args.ckpt else tf.train.latest_checkpoint(logdir2)
    session_inits = []
    if ckpt2:
        session_inits.append(SaverRestore(ckpt2))
    if ckpt1:
        session_inits.append(SaverRestore(ckpt1, ignore=['global_step']))
    pred_conf = PredictConfig(
        model=model,
        input_names=get_eval_input_names(),
        output_names=get_eval_output_names(),
        session_init=ChainInit(session_inits))
    predictor = OfflinePredictor(pred_conf)

    audio, y_audio, ppgs = convert(predictor, df)

    # TODO make me into an input
    args.output_path = '/freeman_data/inference/test_output.wav'

    write_wav(audio[0], hp.default.sr, args.output_path)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('case1', type=str, help='experiment case name of train1')
    parser.add_argument('case2', type=str, help='experiment case name of train2')
    parser.add_argument('-ckpt', help='checkpoint to load model.')
    # TODO: make these into mandatory positional arguments
    parser.add_argument('-input_path', help='absolute path to input .wav file')
    parser.add_argument('-output_path', help='absolute path to output .wav file')
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    args = get_arguments()
    hp.set_hparam_yaml(args.case2)
    logdir_train1 = '{}/{}/train1'.format(hp.logdir_path, args.case1)
    logdir_train2 = '{}/{}/train2'.format(hp.logdir_path, args.case2)

    print('case1: {}, case2: {}, logdir1: {}, logdir2: {}'.format(args.case1, args.case2, logdir_train1, logdir_train2))

    s = datetime.datetime.now()

    do_convert(args, logdir1=logdir_train1, logdir2=logdir_train2)

    e = datetime.datetime.now()
    diff = e - s
    print("Done. elapsed time:{}s".format(diff.seconds))
