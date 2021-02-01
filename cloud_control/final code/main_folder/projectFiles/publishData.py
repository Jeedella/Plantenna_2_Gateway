#Author: Omar Mhaouch
#Date: 26-01-2021
#Last updated: 26-01-2021

#This script is used to send the data coming from the NRF to the dashboard.
#This script is purely to send data. The connection is handled in mqttConnect.py


import paho.mqtt.client as mqtt
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

    try:
        client.publish('v1/devices/me/telemetry', json.dumps(deviceData), 1)
    except Exception as e:
        print(f"Could not publish data, {e}")
        
if __name__ == "__main__":
    init()

