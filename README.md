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

## Working with Bluepy
These instructions will make use of other tutorials to save space in this document, since it is supposed to be at least reasonably consise. It is important to mention that the file to provide a demo for BLE pairing (NRF52Rpi_BLE_ChargeCapModel.py) requires the NRF52 to have the "BLE peripheral/BLE blinky application" from the Nordic Semiconductor examples loaded into it (info about this application: https://infocenter.nordicsemi.com/index.jsp?topic=%2Fsdk_nrf5_v17.0.0%2Fble_sdk_app_hrc.html)

Therefore, make sure you have Segger Embedded Studio installed. To do this, follow the relevant part this tutorial: https://hackmd.io/@sookah/myAir. It will explain how to install segger and how to be able to load an example program into the nRF52. The tutorial uses NRFconnect for this, while the Youtube video, that the tutorial refers to, opens Segger projects directly from the downloaded folders instead. Use whichever option you prefer.

After the BLE Blinky example application has been loaded, refer to this repository: https://github.com/rlangoy/bluepy_examples_nRF51822_mbed. It contains information about its content and a tutorial on how to use the python scripts on the Raspberry pi. Please note that these scripts are meant for a contact with the nRF51822 rather than the nRF52-DK and that the example used is therefore also different. For most of the scripts this does not matter, since they are not dependant on Bluetooth UUID's to be entered into the script itself. With this, I am primarily refering to blesca.py, getDesc.py, getDeviceCharacteristics.py, getServices.py. it is possible that others work immediately as well.

Finally, a short explanation of Bluetooth LE pairing with the Pi is necessary along with what the earlier mentioned file contains and is capable of. The main code necessary for getting contact with the nRF is using its MAC-address. This is also what to use when calling a number of the python scripts from the other repository, as is mentioned there. To be able to read or write data, one first needs to know the UUID (universally unique identifier) of the bluetooth service controlling the desired function. Contained within the provided services are characteristics, which hold the data to be read or written. Characteristics also have their own UUID, which is also necessary when wanting to change, in this case, the LED value or read the current button state. The python scripts mentioned above all have a scanning function to be able to find out more about the device one is trying to connect. 
The file is this repository, NRF52Rpi_BLE_ChargeCapModel.py, uses the basics from readButton1.py and writeLed2.py to create a script that causes the nRF52 to function as a model of a charging capacitor. Pressing Button1 on the nRF will cause the "capacitor" to charge (voltage values will be printed on the Pi's terminal) and discharge as soon as the button is released. When the capacitor is close to reaching it's final value, LED3 will light up and turn off whenever the voltage drops below that value. Naturally, this model was not the aim of this project, but a program had to be written that was able to showcase interesting visuals, based on simple inputs. Unfortunately, the final connection, the one between the gateway and the IoT platform was unfortunately not properly achieved, meaning that the virtual voltage values could not be shown in a graph (more details in the "To-do list" below).    

## Current status of the project
1. bluez meshctl
- bluez meshctl on the Raspberry Pi is working with multiple nRF52-DKs. It was tested with 3 different devices (all running Zephyr.hex), but it should be possible to use more.\

2. bluepy
- Connection between NRF52 and Raspberry Pi has been fully established and tested. Any program that utilizes Bluetooth LE loaded to the NRF52 can be controlled by the Raspberry Pi as long as the correct UUID's are used in the python code. Connecting the Pi to the AWS IoT server has also been proved successfull, but controlling the NRF52 through connection with the Pi on AWS could not be achieved.  

## To-do list
\
bluez:
- Research into the specific meaning and syntax of steps 10 to 13 in the bluez mesctl with Zephyr guide;
- Research into the useability of all other commands from meshctl (after starting meshctl type: "help" without "s in all menus); and
- Research into using Zephyr RTOS for creating BLE mesh nodes on the nRF52-DKs (see node repo of this project).\
\
bluepy:
- Research into how to achieve control over the NRF52 through the AWS IoT server using the Pi as a gateway. The file "NRF52Rpi_BLE_ChargeCapModel_IoT.py" is the code thought to be able to achieve this, but failed. It was loaded onto AWS, connection with the Pi was established, but no response came from the pi in the shape of messages, nor did the NRF52 indicate connection was being made with the Pi. The file is an attempt at integrating both the basic AWS readout code (greengrassHelloWorld) and the ChargeCapModel pi code into one. (see IoT repo of this project for more info); and
- Research into whether Bluetooth LE mesh is possible using the type of bluetooth pairing bluepy makes use of.\
