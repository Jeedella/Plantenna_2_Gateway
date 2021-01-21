import paho.mqtt.client as mqtt
import json
from time import sleep
import sys
INTERVAL = 2
# client = None

deviceData = {
    'Temperature': 0,
    'Humidity' : 0,
    'Pressure' : 0,
    'Airflow' : 0,
    'BatteryLevel' : 0
}


# def loadConfigData():    
#     try:
#         with open("config.json", 'r') as config_file:
#             data = json.load(config_file)
#         return data
#     except Exception as e:
#         print(f'Could not load config file, {e}')

# def getToken(deviceName, configData):
#     try:
#         token = configData[deviceName]['ACCESSTOKEN']
#         print(token)
#         return token
#     except Exception as e:
#         print(f'could not retrieve access token, {e}')
        
# def clientName(deviceName):
#     global client
#     client = 'client'+ deviceName
#     print(client)
#     return client


# value determines connect or disconnect
print("Trying to create an MQTT connection")
clientPA001 = mqtt.Client()
clientPA001.username_pw_set('2P0YswIskauBVegsjRR3')
clientPA001.connect('plantenna.nl', 1883, 60)
clientPA001.loop_start()
print("Connection succesful")

def main():
    while True:
        deviceData['Temperature'] = 10
        deviceData['Humidity'] = 10
        deviceData['Pressure'] = 10
        deviceData['Airflow'] = 10
        deviceData['BatteryLevel'] = 50

        clientPA001.publish('v1/devices/me/telemtry', json.dumps(deviceData), 1)
        sleep(2)

# def mqttConnectDevice(deviceName, token):
#     # client = clientName(deviceName)
#     # value determines connect or disconnect
#     print("Trying to create an MQTT connection")
#     clientPA001 = mqtt.Client()
#     clientPA001.username_pw_set(token)
#     clientPA001.connect('plantenna.nl', 1883, 60)
#     clientPA001.loop_start()
#     print("Connection succesful")
#     return clientPA001

# def publishData(client, temperature, humidity, pressure, airflow, batterylevel):
#     # client = clientName(deviceName)
#     deviceData['Temperature'] = temperature
#     deviceData['Humidity'] = humidity
#     deviceData['Pressure'] = pressure
#     deviceData['Airflow'] = airflow
#     deviceData['BatteryLevel'] = batterylevel

#     client.publish('v1/devices/me/telemtry', json.dumps(deviceData), 1)
#     sleep(2)


if __name__ == "__main__":
    print("MQTT publish test file")
    main()