# Concept codes for the SPMS Cloud Control
This folder contains code which is/was in development. The scripts can be changed without problems. 

## Main Folder
This folder contains the necessary files to publish and subscribe to the Cloud.
The main script is main.py 
When running this script, the whole cloud package is started, which means sending and receiving data from the cloud is possible. 

### Config
In this folder, the a config.json is included which contains the registered device information

### Project Files
This folder contains the modules needed, to run main.py

mqttConnect.py is the script which connects devices to the Thingsboard instance
publishData.py is the script which published data to Thingsboard
sub.py is the script which listens for messages from Thingsboard

## OLD
This folder contains some old scripts which are not used anymore

registerDevice.py is a script to register devices, which represent NRF52 nodes
readDevice.py is a script which gets information about the registered devices.


