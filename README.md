# facial_landmarks
Education project, which detecting facial landmarks via dlib and creating predictions about camera position for shooting set up
# Installing 
- Install python3 and virtualenv
```bash
sudo apt install python3
sudo apt install virtualenv
```
- Download models and install required libraries via install.sh file:
```bash
. ./install.sh
```
# RUN
You can use three CLI argument:
```
-s --shape - optional argument with path to facial landmarks detector
-d --detector - optional argument with path to frontal face detector
-c --capture - optional argument to select a camera source(RTSP-URL/Webcam)
```
Run script:
```bash
. ./venv/bin/activate
python3 fl_script -c 'rtsp://camera_ip:554/'
```
