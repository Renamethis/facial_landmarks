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
