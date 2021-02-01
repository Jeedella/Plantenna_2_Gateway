# Author Omar Mhaouch
# 5-1-2021

# last updated: 1-2-2021

# This script is written to read and register devices
# that work for the smart plant monitoring system

# the system asks for user input. these inputs are:
# Object name --> JSON object name for the device
# Device name --> Hostname registered to the device
# Device MAC --> MAC address registered on the device
# Device version --> Current software version installed on the device
# Device token --> Token which is used to connect trough MQTT to the dashboard

import sys
import json

#function to register the device
def registerDevice():
    #try to get inputs from the user
    try:
        objectName = input("give object name: ")
        deviceName = input("give the device name: ")
        deviceMAC = input("give the mac address of the device: ")
        deviceVersion = input("give the device software version: ")
        deviceToken = input("give the device access token: ")
        #save all the inputs in a dictionary
        x = {}
        x[objectName] = []
        x[objectName] = {
            objectName: objectName,
            "DeviceName": deviceName,
            "MAC_ADDRESS": deviceMAC,
            "nodeVersion": deviceVersion,
            "ACCESSTOKEN": deviceToken
        }
        #open the config file
        with open("config/config.json", "r+") as config_file:
            data = json.load(config_file) #load the file
            data.update(x) #update the file with the dictionary
            config_file.seek(0) #set cursor to 0
            json.dump(data, config_file, indent=4) #save the changes in the correct format

    except Exception as e:
        print(f'something went wrong, {e}')

#main function
def main():
    #call the function to register the device
    registerDevice()

if __name__ == "__main__":
    main()