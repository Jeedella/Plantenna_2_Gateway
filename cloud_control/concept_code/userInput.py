# Author Omar Mhaouch
# This script is used to test user input
# on how to register devices in config.json

import sys
import json

def askForDevice():
    command = input("What do you want? Read/Register?:")
    print(command)
    return command.lower()


def chosenCommand(command):
    if command == "read":
        return "read"
    elif command == "write":
        return "write"


def readCommand():
    with open("testConfig.json", "r") as config_file:
        data = json.load(config_file)
    config_object = input("specify object to be read: ")
    print(data[config_object])


def writeCommand():
    objectType = input("Single or Nested: ")
    if objectType == "standard":
        addObject = input("Register object? yes/no ")
        if addObject == "yes":
            objectName = input("give object name ")
            objectValue = input("give object value ")
        x = {
            objectName: objectValue
        }

    elif objectType == "nested":
        addObject = input("Register object? yes/no: ")
        if addObject == "yes":
            objectName = input("give object name: ")
            deviceName = input("give the device name: ")
            deviceMAC = input("give the mac address of the device: ")
            deviceVersion = input("give the device software version: ")
            deviceToken = input("give the device access token: ")
            x = {}
            x[objectName] = []
            x[objectName] = {
                objectName: objectName,
                "DeviceName" : deviceName,
                "MAC_ADDRESS" : deviceMAC,
                "nodeVersion" : deviceVersion,
                "ACCESSTOKEN" : deviceToken
            }

    with open("testConfig.json", "r+") as config_file:
        data = json.load(config_file)
        data.update(x)
        config_file.seek(0)
        json.dump(data, config_file, indent=4)


if __name__ == "__main__":
    # temp = askForDevice()
    # print(chosenCommand(temp))
    # readCommand()
    writeCommand()
