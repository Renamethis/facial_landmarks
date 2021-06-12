### FACIAL LANDMARKS
import dlib
import cv2
from imutils import face_utils
import imutils
import numpy as np
import argparse
### SETUP ARGUMENT PARSER
parser = argparse.ArgumentParser(description='')
parser.add_argument("-s", "--shape", default = 'shape_predictor_68_face_landmarks.dat',
        help="Path to facial landrmarks detector")
parser.add_argument("-d", "--detector", default = 'mmod_human_face_detector.dat',
        help="Path to frontal face detector")
parser.add_argument("-c", "--capture", default = 'Webcam',
        help="Getting a video image method(Webcam/RTSP_URL/file)")
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
                while(cap.read() != None):
                        pass
        except:
                print('No acces to the source. Check rtsp url')
while cap.isOpened():
    ret, frame = cap.read()
    [height, width, ch] = frame.shape
    print(height, ' ', width)
    image = imutils.resize(frame, width=500)
    xscale = width/image.shape[1]
    yscale = height/image.shape[0]
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rects = detector(rgb, 0)
    for rect in rects:
        rect = rect.rect
        face = predictor(rgb, rect)
        face = face_utils.shape_to_np(face)
        cv2.line(frame, (int(face[41][0]*xscale), int(face[41][1]*yscale)), (int(face[28][0]*xscale), int(face[28][1]*yscale)), (0, 255, 255), 1)
        cv2.line(frame, (int(face[46][0]*xscale), int(face[46][1]*yscale)), (int(face[28][0]*xscale), int(face[28][1]*yscale)), (0, 255, 255), 1)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        for (x, y) in face:
                cv2.circle(frame, (int(x*xscale),int(y*yscale)), 1, (0, 0, 255), -1)
    cv2.line(frame,(int(width/3), 0), (int(width/3), height), (40, 40, 40), 1)
    cv2.line(frame,(int(2*width/3), 0), (int(2*width/3), height), (40, 40, 40), 1)
    cv2.line(frame,(0, int(height/3)), (width, int(height/3)), (40, 40, 40), 1)
    cv2.line(frame,(0, int(2*height/3)), (width, int(2*height/3)), (40, 40, 40),1)
    cv2.imshow('Check', np.array(frame, dtype = np.uint8 ))
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cv2.destroyAllWindows()
