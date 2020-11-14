# Project Smart Plant Monitoring System - Raspberry Pi Gateway
This repository contains all code, guides and other necessary information for the gateway of the Smart Plant Monitoring System (SPMS) Fontys project.\
The gateway is split into 2 parts: 1). BLE network, and 2). local_storage + IoT connection. The BLE network will be upgraded to a BLE mesh network in later versions. See corresponsing subdirectories and README for more information.\
Throughout this project, the Raspberry Pi 4 is used as gateway.


## main control
The main control of the gateway is performed by main_control.py. This python script uses bluepy for BLE network control, and a MQTT to send data to the cloud. In later updates a local storage and 'write control' will be added. With 'write control', the user can write to one or multiple nodes.

## Current status
- Can control BLE network and send data to cloud.

### To-do list
- Add local storage to main control
- Update main_control in such a way that the 'write-value' is only written when needed (instead of every 15 seconds).
