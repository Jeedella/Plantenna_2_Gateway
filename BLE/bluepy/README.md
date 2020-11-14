# Project Smart Plant Monitoring System - Raspberry Pi Gateway - BLE network based on the bluepy library
This README shows how to install the important libraries and how to work with bluepy.\
In addition, the current status of the gateway using bluepy and a to-do list are added below.\
NOTE: Throughout this part of the project, Python version 2.7 was used. To check your current Python version, use the command:
```bash
python --version
```

## Installing bluepy
Normally the bluepy is already installed on the Raspberry Pi.
To be sure you have it installed, type the following command in the terminal:
```bash
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
```
When not installed, you will be asked to install it. Otherwise, you will get a message that it is already installed or it is already the newest version. Then you are already good to go.
For more information or if any problems occur, please refer to [Ian Harvey's bluepy repo](https://github.com/IanHarvey/bluepy).

## Working with bluepy on the Raspberry Pi
A short explanation of Bluetooth LE pairing with the Pi is necessary along with what the earlier mentioned file contains and is capable of. The main code necessary for getting contact with the nRF is using its MAC address. This is also what to use when calling several of the python scripts from the other repository, as is mentioned there. To be able to read or write data, one first needs to know the UUID (universally unique identifier) of the bluetooth service controlling the desired function. Contained within the provided services are characteristics, which hold the data to be read or written. Characteristics also have their own UUID, which is also necessary when wanting to change, in this case, the LED value or read the current button state. The python scripts mentioned above all have a scanning function meant to find out about these UUIDs and other information of the device one is connecting to. 
The file is this repository, NRF52Rpi_BLE_ChargeCapModel.py, uses the basics from readButton1.py and writeLed2.py to create a script that causes the nRF52 to function as a model of a charging capacitor. Pressing Button1 on the nRF will cause the "capacitor" to charge (voltage values will be printed on the Pi's terminal) and discharge as soon as the button is released. When the capacitor is close to reaching it's final value, LED3 will light up and turn off whenever the voltage drops below that value. Naturally, this model was not the aim of this project, but a program had to be written that was able to showcase interesting visuals, based on simple inputs. Unfortunately, the final connection, the one between the gateway and the IoT platform was unfortunately not properly achieved, meaning that the virtual voltage values could not be shown in a graph (more details in the "To-do list" below). Note that the two Bluepy Python scipts in this repository are written in Python 2.7.

The following webpages have been used to help with Python and bluepy coding:
- https://docs.python.org/3/
- https://ianharvey.github.io/bluepy-doc/

## Current status of the gateway using bluepy
- Connection between a single nRF52 and the Raspberry Pi has been fully established and tested. Any program that utilizes BLE loaded to the nRF52 can be controlled by the Raspberry Pi as long as the correct "Complete Local Name" is specified. Note: you may need to (manually) add specific services and/or task (characteristics) to my_ble_names dictonary when the software on the nRF52 is updated.
- The BLE_network class can be used to ease the use of the bluepy libray. This is tested and working. Currently, read values from tasks are only printed and not saved.
- A main file for controlling your networks (main_network_control.py) is tested and working. Currently, the value, which is written to tasks, is a static value and is written every 15 seconds.

## To-do list
programming:
- Update save_tasks so that the read values are saved in the local_storage (instead of only printed).
- Update write_tasks so that the 'write-value' from the local_storage is written (instead of a static value).

resreach:
- Research into whether BLE mesh is possible using the type of bluetooth pairing bluepy makes use of.
