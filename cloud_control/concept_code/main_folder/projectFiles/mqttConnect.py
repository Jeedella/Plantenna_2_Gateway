import paho.mqtt.client as mqtt
import json
from time import sleep
import sys

# client = None

def INIT():

    global THINGSBOARD_HOST 
    THINGSBOARD_HOST = 'plantenna.nl'

    INTERVAL = 2
    
    # global deviceData
    # deviceData = {
    #     'Temperature': 0,
    #     'Humidity' : 0,
    #     'Pressure' : 0,
    #     'Airflow' : 0,
    #     'BatteryLevel' : 0
    # }
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


def mqttConnectDevice(deviceName, token):
    client = clientName(deviceName)
    # value determines connect or disconnect
    print("Trying to create an MQTT connection")
    client = mqtt.Client()
    client.username_pw_set(token)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()
    print("Connection succesful")
    return client



if __name__ == "__main__":
    print("MQTT publish test file")
    INIT()
    data = loadConfigData()
    # token1 = getToken("PA001", data)
    client1 = mqttConnectDevice("PA001", '2P0YswIskauBVegsjRR3')
    while True:
        # publishData(client1, 22, 10, 100, 50, 45)
        print("data sent")