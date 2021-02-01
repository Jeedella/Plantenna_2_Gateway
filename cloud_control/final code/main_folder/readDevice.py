#Author Omar Mhaouch
#5-1-2021

#This script is used to read device information in config.json

#User is asked to input object name

import sys
import json

def getObjectType():
    try: 
        objectType = input("What type is the object? Single/Nested?: ")
        return objectType.lower()
    except Exception as e:
        print(f'Something went wrong, {e}')

def chosenObjectType(objectType, configData):
    if objectType == "single":
        readSingleObject(configData)
    elif objectType == "nested":
        readNestedObject(configData)
    else: print("Wrong input")

def readSingleObject(configData):
    try:
        readObject = input("Give the object name to be read: ")
        print(readObject, ":", configData[readObject])
    except Exception as e:
        print(f"Read error, check your input!, {e}")

def readNestedObject(configData):
    try:
        readObject = input("Give the object name to be read: ")
        readNested = input("Give the nested object name to be read: ")
        print(readNested, ":", configData[readObject][readNested])
    except Exception as e:
        print(f"Read error, check your input!, {e}")

def loadConfigData():
    try:
        with open("config/config.json", 'r') as config_file:
            data = json.load(config_file)
        return data
    except Exception as e:
        print(f'Could not load config file, {e}')

def main():
    data = loadConfigData()
    objectType = getObjectType()
    try:
        chosenObjectType(objectType, data)
    except Exception as e:
        print(f"Wrong object, {e}")
    


if __name__ == "__main__":
    # data = loadConfigData()
    # objectType = getObjectType()
    # chosenObjectType(objectType, data)
    main()