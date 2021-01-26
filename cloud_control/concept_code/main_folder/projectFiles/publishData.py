import paho.mqtt.client as mqtt
import sys
from time import sleep
import json

def init():
    global deviceData	
    # create a JSON dictionary to set the initial values
    deviceData = {
        'Temperature': None,
        'Humidity' : None,
        'Pressure' : None,
        'Airflow' : None,
        'BatteryLevel' : None
    }
    return

def publishData(client, temperature, humidity, pressure, airflow, batterylevel):
    
    deviceData['Temperature'] = temperature
    deviceData['Humidity'] = humidity
    deviceData['Pressure'] = pressure
    deviceData['Airflow'] = airflow
    deviceData['BatteryLevel'] = batterylevel

    client.publish('v1/devices/me/telemetry', json.dumps(deviceData), 1)

# if __name__ == "__main__":
    # init()
    # INIT()
    # loadConfigData()
    # token1 = getToken("PA001")
    # token2 = getToken("PA002")   
    # client1 = mqttConnectDevice("PA001", token1, 0)
    # client2 = mqttConnectDevice("PA002", token2, 0)
    # publishData(client1, 22, 10, 100, 50, 70, 45)

