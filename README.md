# Project Plant Sensing System - Raspberry Pi Gateway
This README shows how to install the important libraries, how to start bluez meshctl, and the possible problems and solutions with bluez.

## Installing bluez and bluepy
Step 1. Install bluez
Follow this document to install bluez: "Tutorial-How-to-set-up-BlueZ.pdf"

Step 2. Install bluepy
Normally the bluepy is already installed on the Raspberry Pi.
To be sure you have it installed, type the following command in the terminal:
```bash
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
```
When not installed, you will be asked to install it. Otherwise, you will get a message that it is already installed or it is already the newest version. Then you are already good to go.
For more information or if any problems occur, please refer to the Ian Harvey's bluepy github at: https://github.com/IanHarvey/bluepy

## How to start bluez meshctl
When bluez is installed correctly, meshctl can be found in the folder bluez-5.50/mesh. Please replace "5.50" by your version of bluez.
You can check your version of bluez and meshctl with the command:
```python
bluetoothd -v
meshctl -v
```

Type the following command to start meshctl:
```python
meshctl
```

The following should appear on the terminal:
```bash
pi@raspberrypi:~/bluez-5.50/mesh $ meshctl
[meshctl]# 
```
If any problems occur, please refer to the next chapter.

## Possible problems and solutions with bluez
The following list gives all possible problems that could occur after installing or after changing some files from bluez:

1. local_node.json
When trying to start meshctl and this message appears:
```bash
failed to parse local node configuration file local_node.json
```
something went wrong during step 3 of installing bluez. Please repeat step 3.0 up to step 3.5 and the problem should be solved. If not, please redo all steps and try again.