import paho.mqtt.client as mqtt
from time import sleep

def init():

    # create a JSON dictionary to set the initial values
    deviceData = {
        'Temperature': None,
        'Humidity' : None,
        'Pressure' : None,
        'Airflow' : None,
        'BatteryLevel' : None
    }

def publishData(temperature, humidity, pressure, airflow, batterylevel):
    deviceData['Temperature'] = temperature
    deviceData['Humidity'] = humidity
    deviceData['Pressure'] = pressure
    deviceData['Airflow'] = airflow
    deviceData['BatteryLevel'] = batterylevel

    client.publish('v1/devices/me/telemtry', json.dump(deviceData), 1)
    sleep(2)

if __name__ == "__main__":
    init()
    publishData()

