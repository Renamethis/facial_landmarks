#!/bin/bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
wget https://github.com/davisking/dlib-models/raw/master/mmod_human_face_detector.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d mmod_human_face_detector.dat.bz2
rm -rf *.bz2
virtualenv --system-site-packages -p python3 venv
. ./venv/bin/activate
git clone https://github.com/FalkTannhaeuser/python-onvif-zeep.git
cd python-onvif-zeep
python3 setup.py install
pip3 install --upgrade onvif_zeep
cd ..
python3 -m pip install -r requirements.txt
. ./build_opencv.sh
