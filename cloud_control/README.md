# Project Plant Sensing System - Raspberry Pi Gateway - cloud_control
This README contains the status of the cloud_control of the Gateway. Also, a To-do list is provided.

## Installing dependencies
To use the cloud control several libraries must be installed.\
Make sure to use pip install instead of pip3 install, since python 2 is used throughout this project.\
\
smbus2:
```bash
sudo pip install smbus2
```
\
bme280:
```bash
sudo pip install bme280
```
\
paho.mqtt.client:
```bash
sudo pip install paho-mqtt
```

## Initialize the MQTT communication
To send data through the MQTT protocol, it is necessary to configure a few parameters:
**THINGSBOARD_HOST=**'*your url here*'
This can be an IP address or URL of where your Thingsboard instance is running
**ACCESS_TOKEN=**'*your device token here*'
This is the token generated when creating a device on Thingsboard. This token can be copied and is valid for one device.

## Sending data
To send data, a library name paho-mqtt is used. This is a python library which makes mqtt communication possible. More info about this library, please refer to [paho-mqtt website](https://pypi.org/project/paho-mqtt/)
Sending data is done using the *publish* command
This command contains the location to where the data is published, and the data itself.
```client.publish('v1/devices/me/telemetry', json.dumps(**your function**), 1)```

## Current status
It is possible to receive data from the NRF52 and show it on the Thingsboard Dashboard. 
For more info about data visualisation please refer to the [Plantenna Cloud Repository](https://github.com/Jeedella/Plantenna_2_Cloud)

## ToDo
Add reverse communication functionality, which subscribes to the dashboard and listens if any commands are generated.
Remote Firmware updates
Script for device registration

