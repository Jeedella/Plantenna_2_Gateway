# Project Plant Sensing System - Raspberry Pi Gateway
This README shows how to install the important libraries, how to start bluez meshctl, and the possible problems and solutions with bluez./
In addition, the current status of this project and the to-do list are added below.

## Installing bluez and bluepy
Step 1. Install bluez\
Follow this guide to install bluez: "Tutorial-How-to-set-up-BlueZ.pdf"

Step 2. Install bluepy\
Normally the bluepy is already installed on the Raspberry Pi.
To be sure you have it installed, type the following command in the terminal:
```bash
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
```
When not installed, you will be asked to install it. Otherwise, you will get a message that it is already installed or it is already the newest version. Then you are already good to go.
For more information or if any problems occur, please refer to Ian Harvey's bluepy repo at: https://github.com/IanHarvey/bluepy

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
If any problems occur, please refer to the next chapter in this README.
Chapter 3 and onwards in the guide "Tutorial-How-to-set-up-BlueZ_Part2-3.pdf" shows how to use the bluez meschtl. Use the nRF52-DK and run the program Zephyr.hex on it. This program spits out the provisioning key on a serial terminal, like PuTTY (install here: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). The nRF52-DK's micro-USB input should be connected to the USB input of the PC (or any other device with a serial monitor).
In addition, a step-by-step guide with pictures ("Step-by-step-guide-meshctl-with-Zephyr.pdf") is also provided. The program Zephyr.hex was running on the nRF5-DK and PuTTY was installed on a Windows 10 laptop.

## Possible problems and solutions with bluez
The following list gives all possible problems that could occur after installing or after changing some files from bluez:

1. local_node.json\
When trying to start meshctl and this message appears:
```bash
failed to parse local node configuration file local_node.json
```
something went wrong during step 3 of installing bluez. Please repeat step 3.0 up to step 3.5 and the problem should be solved. If not, please redo steps 2.2, 2.5 - 3.5 (re-install bluez-5.50 and update kernel) and try again (be user to remove the bluez-5.50 directory first). If it still fails, try to redo the entire guide (first remove all).

## Current status of the project
1. bluez meshctl
- bluez meshctl on the Raspberry Pi is working with multiple nRF52-DKs. It was tested with 3 different devices (all running Zephyr.hex), but it should be possible to use more.\

2. bluepy
- Connection between NRF52 and Raspberry Pi has been fully established and tested. Any program that utilizes Bluetooth LE loaded to the NRF52 can be controlled by the Raspberry Pi as long as the correct UUID's are used in the python code. Connecting the Pi to the AWS IoT server has also been proved successfull, but controlling the NRF52 through connection with the Pi on AWS could not be achieved.  

## To-do list
- Add explanation about using bluepy to README + update README (@Corstiaan) -- remove this when done\
\
bluez:
- Research into the specific meaning and syntax of steps 10 to 13 in the bluez mesctl with Zephyr guide;
- Research into the useability of all other commands from meshctl (after starting meshctl type: "help" without "s in all menus); and
- Research into using Zephyr RTOS for creating BLE mesh nodes on the nRF52-DKs (see node repo of this project).\
\
bluepy:
- Research into how to achieve control over the NRF52 through the AWS IoT server using the Pi as a gateway. The file "NRF52Rpi_BLE_ChargeCapModel_IoT.py" is the code thought to be able to achieve this, but failed. It was loaded onto AWS, connection with the Pi was established, but no response came from the pi in the shape of messages, nor did the NRF52 indicate connection was being made with the Pi. The file is an attempt at integrating both the basic AWS readout code (greengrassHelloWorld) and the ChargeCapModel pi code into one. (see IoT repo of this project for more info); and
- Research into whether Bluetooth LE mesh is possible using the type of bluetooth pairing bluepy makes use of.\
