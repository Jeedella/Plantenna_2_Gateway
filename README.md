# Project Smart Plant Monitoring System - Raspberry Pi Gateway
This repository contains all code, guides and other necessary information for the gateway of the Smart Plant Monitoring System (SPMS) Fontys project.\
The gateway is split into 2 parts: 1). BLE network, and 2). local_storage + IoT connection. The BLE network will be upgraded to a BLE mesh network in later versions. See corresponsing subdirectories and README for more information.\
Throughout this project, the Raspberry Pi 4 is used as gateway.


## main control
The main control of the gateway is performed by main_control.py. This python script uses bluepy for BLE network control, and MQTT to send data to the cloud. In later updates a local storage and 'write control' will be added. With 'write control', the user can write to one or multiple nodes.\
NOTE: When both broadcast data and notify/read/write are active, broadcast data and/or notify messages can be missed (see [to-do list](#To-do-list) below).

## Current status
- Can control BLE network: Discover devices, add/remove devices, send data, receive data via read/notify/broadcast.
- Send data to cloud.

## To-do list
- Add local storage to main control
- Update main_control in such a way that the 'write-value' is only written when needed (instead of every 15 seconds).
- main_control can be updated in such a way that notify and broadcast data can always be read (only when active/needed). The current code waits for notification (and afterwards can do read/write). Then it waits for broadcast data. No notify can be received when waiting for broadcast data, and also the other way around. It may be possible that data is missed in the meantime.
