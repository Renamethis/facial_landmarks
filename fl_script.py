### FACIAL LANDMARKS
import dlib
import cv2
from imutils import face_utils
import imutils
import numpy as np
import argparse
from math import sqrt
### SETUP ARGUMENT PARSER
parser = argparse.ArgumentParser(description='')
parser.add_argument("-s", "--shape", default = 'shape_predictor_68_face_landmarks.dat',
        help="Path to facial landrmarks detector")
parser.add_argument("-d", "--detector", default = 'mmod_human_face_detector.dat',
        help="Path to frontal face detector")
parser.add_argument("-c", "--capture", default = 'Webcam',
        help="Getting a video image method(Webcam/RTSP_URL/file)")
parser.add_argument("-w", "--write", default = 'None',
        help="Filename of output file or None")
args = vars(parser.parse_args())

### INIT DLIB DETECTORS

detector = dlib.cnn_face_detection_model_v1(args['detector'])
predictor = dlib.shape_predictor(args['shape'])
### CAPTURE VIDEO STREAM FROM DEVICE
if(args['capture'] == 'Webcam'):
        cap = cv2.VideoCapture(0)
else:
    try:
        cap = cv2.VideoCapture(args['capture'])
        while(cap.read() is None):
            pass
    except:
        print('No acces to the source. Check rtsp url')
(ret, frame) = cap.read()
[height, width, ch] = frame.shape
if(args['write'] != 'None'):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args['write'], fourcc, 20.0, (width, height))
while cap.isOpened():
    ret, frame = cap.read()
    if(ret is None or frame is None):
        break
    image = imutils.resize(frame, width=1500)
    xscale = width/image.shape[1]
    yscale = height/image.shape[0]
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rects = detector(rgb, 0)
    for rect in rects:
        rect = rect.rect
        face = predictor(rgb, rect)
        face = face_utils.shape_to_np(face)
        center = (int(face[30][0]*xscale), int(face[30][1]*yscale))
        (x41, y41) = (int(face[41][0]*xscale), int(face[41][1]*yscale))
        (x28, y28) = (int(face[28][0]*xscale), int(face[28][1]*yscale))
        (x46, y46) = (int(face[46][0]*xscale), int(face[46][1]*yscale))
        lenL = sqrt((x28 - x41)*(x28 - x41) + (y28 - y41)*(y28 - y41))
        lenR = sqrt((x28 - x46)*(x28 - x46) + (y28 - y46)*(y28 - y46))
        string = ""
        Color = (0, 0, 0)
        if(abs(lenL - lenR) < 1):
            string = "Frontal shooting"
            Color = (0, 255, 0)
        else:
            if(lenL > lenR):
                pos = (width/3)
            else:
                pos = (2*width/3)
            if(center[0] < pos + 15 and center[0] > pos - 15):
                string = "Correct location in third"
                Color = (0, 255, 0)
            else:
                Color = (0, 0, 255)
                string = "Move camera to " + ('left' if lenL > lenR else 'right')
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
    cv2.imshow('Check', np.array(frame, dtype = np.uint8 ))
    if(args['write'] != 'None'):
        out.write(frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cv2.destroyAllWindows()
