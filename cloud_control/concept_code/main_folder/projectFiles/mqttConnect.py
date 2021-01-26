#Author: Omar Mhaouch
#Date: 26-01-2021
#Last updated: 26-01-2021

# This script is used to create a connection with the 
# Thingsboard dashboard. An MQTT connection is established using
# the correct credentials


import paho.mqtt.client as mqtt
import json
from time import sleep


def INIT():

    global THINGSBOARD_HOST 
    THINGSBOARD_HOST = 'plantenna.nl'

    INTERVAL = 2
    return


def loadConfigData():    
    try:
        with open("config/config.json", 'r') as config_file:
            data = json.load(config_file)
        return data
    except Exception as e:
        print(f'Could not load config file, {e}')

def getToken(deviceName, configData):
    try:
        token = configData[deviceName]['ACCESSTOKEN']
        print(token)
        return token
    except Exception as e:
        print(f'could not retrieve access token, {e}')
        
def clientName(deviceName):
    global client
    client = 'client'+ deviceName
    print(client)
    return client


def mqttConnectDevice(client, token):
    connected = False
    try:
        print("Trying to create an MQTT connection")
        client = mqtt.Client()
        client.username_pw_set(token)
        client.connect(THINGSBOARD_HOST, 1883, 60)
        client.loop_start()
        connected = True
        if connected == True:
            print("Connection succesful")
            return client
    except Exception as e:
        print(f"could not establish connection, {e}")

if __name__ == "__main__":
    print("MQTT publish test file")
    INIT()
    data = loadConfigData()
    client1 = mqttConnectDevice("PA001", '2P0YswIskauBVegsjRR3')
    while True:
        print("data sent")