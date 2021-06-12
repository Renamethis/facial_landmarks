#!/bin/bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
wget https://github.com/davisking/dlib-models/raw/master/mmod_human_face_detector.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d mmod_human_face_detector.dat.bz2
python3 -m venv venv
. ./venv/bin/activate
python3 -m pip install -r requirements.txt
git clone https://github.com/davisking/dlib.git
cd dlib
python3 setup.py install --set DUSE_AVX_INSTRUCTIONS=1 --set DUSE_AVX_INSTRUCTIONS=1
