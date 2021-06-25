# facial_landmarks
Education project, which detecting facial landmarks via dlib and creating predictions about camera position for shooting set up

You can use this project in two modes:
- Onvif autocontrol
- Operator Hints
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
# CREATE CONFIG
Run config creating script and enter necessary information
```bash
python3 create_config.py
```
# CONfIG OPTIONS
- Section ONVIFSettings

  'ptz' - (False/True) - enable/disable onvif autocontroller
  
  'speed' - (0;1) - speed of camera movement
  
  'ip' - (string) - ip address of onvif camera
  
  'port' - (0;65535) - port of onvif camera
  
  'user' - (string) - username of onvif user
  
  'password' - (string) - password of onvif user
  
  'profile' - (0/1) - media profile for rtsp stream grabbing(sub/main)
  
- Section MAINSettings

  'source' - string - input source for video capturing
  
  'leftpoint' - (0;67) - index point of left eye
  
  'rightpoint' - (0;67) - index point of right eye
  
  'nosepoint' - (0;67) - index point of nose
  
  'centerpoint' - (0;67) - index point of center
  
  'turndifferent' - (0;1980) - amount of pixels, which be ignored by direction of gaze detector
  
  'thirddifferent' - (0;1980) - amount of pixels of third zones
  
  'imagewidth' - (0;1980) - width of the image to be sent to dlib detectors
  
# RUN
You can use three CLI argument:
```
-s --shape - optional argument with path to facial landmarks detector
-d --detector - optional argument with path to frontal face detector
```
Run script:
```bash
. ./venv/bin/activate
python3 fl_script
```
Run zeromq client:
```bash
. ./venv/bin/activate
python3 zeromqclient.py
```
