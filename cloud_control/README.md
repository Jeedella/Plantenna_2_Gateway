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

## Current status
- spms_cloud_control.py can be used to submit BME sensor data to ThingsBoard. For more information on the cloud storage itself, please refer to the [cloud repository](https://github.com/Jeedella/Plantenna_2_Cloud). It can be either used as a stand alone or within other scripts.
- spms_cloud_control.py is used in the main_control.py script. Here, the gathered data over BLE is send to the cloud using MQTT.

## To-do list
- Among other things, add 'write control' to spms_cloud_control.py. With 'write control', the user can write to one or multiple nodes.
