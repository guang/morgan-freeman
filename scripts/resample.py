#!/usr/local/bin/python

import librosa
import soundfile as sf
import sys


if __name__ == "__main__":
    path = sys.argv[1]
    out_path = sys.argv[2]
    existing_sr = int(sys.argv[3])
    y, sr = librosa.load(path, sr=existing_sr)
    y_16k = librosa.resample(y, sr, 16000)
    sf.write(file=out_path, data=y_16k, samplerate=16000, subtype="PCM_16")

    # log
    print("resampled from {path} at {sr} to {out_path}".format(
        path=path,
        sr=existing_sr,
        out_path=out_path,
    ))
