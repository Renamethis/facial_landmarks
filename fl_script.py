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
class grabber(Thread):
    frame = None
    ret = None
    def __init__(self, Uri):
        self.Uri = Uri
        self.capture = cv2.VideoCapture(Uri, cv2.CAP_GSTREAMER)
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
### SETUP ARGUMENT PARSER
parser = argparse.ArgumentParser(description='')
parser.add_argument("-s", "--shape", default = 'shape_predictor_68_face_landmarks.dat',
        help="Path to facial landrmarks detector")
parser.add_argument("-d", "--detector", default = 'mmod_human_face_detector.dat',
        help="Path to frontal face detector")
parser.add_argument("-w", "--write", default = 'None',
        help="Filename of output file or None")
args = vars(parser.parse_args())
### INIT ONVIF CAMERA
if(config['ONVIFSettings']['ptz'] == 'True'):
    ip = config['ONVIFSettings']['ip']
    port = config['ONVIFSettings']['port']
    login = config['ONVIFSettings']['user']
    password = config['ONVIFSettings']['password']
    wsdl = 'python-onvif-zeep/wsdl'
    speed = float(config['ONVIFSettings']['speed'])
    controller = OnvifController(ip, port, login, password, wsdl, 0)
### INIT DLIB DETECTORS
print('Initializing DLIB models')
detector = dlib.cnn_face_detection_model_v1(args['detector'])
predictor = dlib.shape_predictor(args['shape'])
print('Models initialized successfully')
### CAPTURE VIDEO STREAM FROM DEVICE
#Uri = controller.getRtspUrl()
Uri = 'rtsp://172.18.191.72/'
Uri = 'rtspsrc location="' + Uri + '" ! rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! appsink'
#cap = cv2.VideoCapture(Uri, cv2.CAP_FFMPEG)
cap = grabber(Uri)
cap.start()
(ret, frame) = cap.read()
while(ret is None or frame is None):
	ret, frame = cap.read()
[height, width] = frame.shape
if(args['write'] != 'None'): ### VIDEO WRITER
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args['write'], fourcc, 20.0, (width, height))
print('Program started')
while cap.isOpened():
    ret, frame = cap.read()
    if(ret is None or frame is None):
        break
    image = imutils.resize(frame, width=600)
    xscale = width/image.shape[1]
    yscale = height/image.shape[0]
    #rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rects = detector(image, 0)
    if(len(rects) > 1):
       print('Several persons in shooting area')
       if(config['ONVIFSettings']['ptz'] == 'True'):
           controller.stop()
       continue
    for rect in rects:
        rect = rect.rect
        face = predictor(image, rect)
        face = face_utils.shape_to_np(face)
        center = (int(face[30][0]*xscale), int(face[30][1]*yscale))
        (x41, y41) = (int(face[41][0]*xscale), int(face[41][1]*yscale))
        (x28, y28) = (int(face[28][0]*xscale), int(face[28][1]*yscale))
        (x46, y46) = (int(face[46][0]*xscale), int(face[46][1]*yscale))
        lenL = sqrt((x28 - x41)*(x28 - x41) + (y28 - y41)*(y28 - y41))
        lenR = sqrt((x28 - x46)*(x28 - x46) + (y28 - y46)*(y28 - y46))
        string = ""
        Color = (0, 0, 0)
        if(abs(lenL - lenR) < 20):
            string = "Frontal shooting"
            Color = (0, 255, 0)
            if(config['ONVIFSettings']['ptz'] == 'True'):
                controller.stop()
        else:
            if(lenL > lenR):
                pos = (width/3)
            else:
                pos = (2*width/3)
            if(center[0] < pos + 75 and center[0] > pos - 75):
                string = "Correct location in third"
                Color = (0, 255, 0)
                if(config['ONVIFSettings']['ptz'] == 'True'):
                    controller.stop()
            elif(center[0] < width/3 - 75 or center[0] > 2*width/3 + 75):
                string = "Place face in center of shooting area"
                if(config['ONVIFSettings']['ptz'] == 'True'):
                    controller.stop()
            else:
                k = (center[0] - pos)/abs(width/2 - pos)
                k = -1 if k < -1 else k
                k = 1 if k > 1 else k
                print('Move koeff : ', k)
                Color = (0, 0, 255)
                if(config['ONVIFSettings']['ptz'] == 'True'):
                    controller.moveCamera((speed if lenL > lenR else -speed), 0)
                string = "Move camera to " + ('right' if lenL > lenR else 'left')
        print(string)
        if(args['write'] != 'None'):
            cv2.line(frame, (x41, y41), (x28, y28), (0, 255, 255), 1)
            cv2.line(frame, (x46, y46), (x28, y28), (0, 255, 255), 1)
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
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
