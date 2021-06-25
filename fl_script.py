### FACIAL LANDMARKS
import dlib
import cv2
from imutils import face_utils
import imutils
import numpy as np
import argparse
from math import sqrt
from onvif import ONVIFCamera
import configparser
import os.path
import sys
from onvif_control import OnvifController
from threading import Thread
import json
import zmq
from zmqserver import zeromq_server
outputdata = {
    'message' : None,
    'detectingData' : None,
}
### INIT ZEROMQ SERVER
server = zeromq_server("tcp://*:5555")
server.start()
### CLASS FOR STREAM CAPTURE
class grabber(Thread):
    frame = None
    ret = None
    def __init__(self, source = None, capflag = None):
        self.source = source
        self.capture = cv2.VideoCapture(0) if capflag == None else cv2.VideoCapture(source, capflag)
        Thread.__init__(self)
    def run(self):
        while self.capture.isOpened():
            self.ret, self.frame = self.capture.read()
    def read(self):
        return [self.ret, self.frame]
    def isOpened(self):
        return self.capture.isOpened()

### INIT CONFIG PARSER
config = configparser.ConfigParser()
if(not os.path.isfile('settings.ini')):
    print('Configuration file is not exists, create it, using create_config.py')
    sys.exit(1)
config.read('settings.ini')

### READ MAIN SETTINGS FROM CONFIG
lpoint = int(config['MAINSettings']['leftpoint'])
rpoint = int(config['MAINSettings']['rightpoint'])
npoint = int(config['MAINSettings']['nosepoint'])
cpoint = int(config['MAINSettings']['centerpoint'])
tnd = int(config['MAINSettings']['turndifferent'])
trd = int(config['MAINSettings']['thirddifferent'])
imagewidth = int(config['MAINSettings']['imagewidth'])
### SETUP ARGUMENT PARSER
parser = argparse.ArgumentParser(description='')
parser.add_argument("-s", "--shape", default = 'shape_predictor_68_face_landmarks.dat',
        help="Path to facial landrmarks detector")
parser.add_argument("-d", "--detector", default = 'mmod_human_face_detector.dat',
        help="Path to frontal face detector")
parser.add_argument("-w", "--write", default = 'None',
        help="Filename of output file or None")
args = vars(parser.parse_args())
### INIT ONVIF CAMERA AND CAPTURE
if(config['ONVIFSettings']['ptz'] == 'True'):
    ip = config['ONVIFSettings']['ip']
    port = config['ONVIFSettings']['port']
    login = config['ONVIFSettings']['user']
    password = config['ONVIFSettings']['password']
    wsdl = 'python-onvif-zeep/wsdl'
    speed = float(config['ONVIFSettings']['speed'])
    controller = OnvifController(ip, port, login, password, wsdl, int(config['ONVIFSettings']['profile']))
    Uri = controller.getRtspUrl()
    source = 'rtspsrc location="' + Uri + '" ! rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! appsink'
    cap = grabber(Uri, cv2.CAP_GSTREAMER)
else:
    source = config['MAINSettings']['source']
    cap = grabber(source , cv2.CAP_FFMPEG) if source != '0' else grabber()

### INIT DLIB DETECTORS
print('Initializing DLIB models')
detector = dlib.cnn_face_detection_model_v1(args['detector'])
predictor = dlib.shape_predictor(args['shape'])
print('Models initialized successfully')
cap.start()
(ret, frame) = cap.read()
while(ret is None or frame is None):
	ret, frame = cap.read()
if(len(frame.shape) == 3):
    [height, width, _] = frame.shape
else:
    [height, width] = frame.shape
if(args['write'] != 'None'): ### VIDEO WRITER
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args['write'], fourcc, 20.0, (width, height))
print('Program started')
while cap.isOpened():
    string = ""
    outputdata['detectingData'] = None
    outputdata['message'] = None
    ret, frame = cap.read()
    if(ret is None or frame is None):
        break
    image = imutils.resize(frame, width=imagewidth)
    xscale = width/image.shape[1]
    yscale = height/image.shape[0]
    rects = detector(image, 0)
    if(len(rects) > 1):
       string = 'Several persons in shooting area'
       if(config['ONVIFSettings']['ptz'] == 'True'):
           controller.stop()
    elif(len(rects) == 0):
         string = 'No persons detected'
         if(config['ONVIFSettings']['ptz'] == 'True'):
             controller.stop()
    else:
        rect = rects[0].rect
        face = predictor(image, rect)
        face = face_utils.shape_to_np(face)
        center = (int(face[cpoint][0]*xscale), int(face[cpoint][1]*yscale))
        (xl, yl) = (int(face[lpoint][0]*xscale), int(face[lpoint][1]*yscale))
        (xn, yn) = (int(face[npoint][0]*xscale), int(face[npoint][1]*yscale))
        (xr, yr) = (int(face[rpoint][0]*xscale), int(face[rpoint][1]*yscale))
        lenL = sqrt((xn - xl)*(xn - xl) + (yn - yl)*(yn - yl))
        lenR = sqrt((xn - xr)*(xn - xr) + (yn - yr)*(yn - yr))
        Color = (0, 0, 0)
        k = 0
        if(abs(lenL - lenR) < tnd):
            k = 0
            string = "Frontal shooting"
            Color = (0, 255, 0)
            if(config['ONVIFSettings']['ptz'] == 'True'):
                controller.stop()
        else:
            if(lenL > lenR):
                pos = (width/3)
            else:
                pos = (2*width/3)
            if(center[0] < pos + trd and center[0] > pos - trd):
                string = "Correct location in third"
                Color = (0, 255, 0)
                if(config['ONVIFSettings']['ptz'] == 'True'):
                    controller.stop()
            elif(center[0] < width/3 - trd or center[0] > 2*width/3 + trd):
                string = "Place face in center of shooting area"
                k = 1 if center[0] < center[0] < width/3 - trd else -1
                if(config['ONVIFSettings']['ptz'] == 'True'):
                    controller.stop()
            else:
                k = (center[0] - pos)/abs(width/2 - pos)
                k = -1 if k < -1 else k
                k = 1 if k > 1 else k
                Color = (0, 0, 255)
                if(config['ONVIFSettings']['ptz'] == 'True'):
                    controller.moveCamera((speed if lenL > lenR else -speed), 0)
                string = "Move camera to " + ('right' if lenL > lenR else 'left')
        outputdata['detectingData'] = {
            'righteye': {
                'x': xr,
                'y': yr
            },
            'lefteye': {
                'x': xl,
                'y': yl
            },
            'nose': {
                'x': xn,
                'y': yn
            },
            'moveRatio': k
        }
        outputdata['message'] = string
        server.set_message(json.dumps(outputdata))
        ### DRAW POINTS AND LINES FOR OUPUT VIDEO
        if(args['write'] != 'None'):
            cv2.line(frame, (xl, yl), (xn, yn), (0, 255, 255), 1)
            cv2.line(frame, (xr, yr), (xn, yn), (0, 255, 255), 1)
            cv2.putText(frame, string, (30, height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, Color, 2, cv2.LINE_AA)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            for (x, y) in face:
                    cv2.circle(frame, (int(x*xscale),int(y*yscale)), 1, (0, 0, 255), -1)
            cv2.line(frame,(int(width/3), 0), (int(width/3), height), (40, 40, 40), 1)
            cv2.line(frame,(int(2*width/3), 0), (int(2*width/3), height), (40, 40, 40), 1)
            cv2.line(frame,(0, int(height/3)), (width, int(height/3)), (40, 40, 40), 1)
            cv2.line(frame,(0, int(2*height/3)), (width, int(2*height/3)), (40, 40, 40),1)
    if(args['write'] != 'None'):
        out.write(frame)
server.stop_thread()
