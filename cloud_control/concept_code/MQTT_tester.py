import paho.mqtt.client as mqtt
import sys
import json
from time import sleep
import random

THINGSBOARD_HOST = 'plantenna.nl'
ACCESS_TOKEN = '2P0YswIskauBVegsjRR3'

INTERVAL = 2

device_data = {'Temperature': None, 'Humidity': None, 'Pressure': None, 'Airflow': None, 'BatteryLevel': None}
global client
client = mqtt.Client()
# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

def main():
    while True:
        randTemperature = random.randint(18, 25)
        randPressure = random.uniform(0.5, 1.5)
        randHumidity = random.randint(30, 50)
        randAirflow = random.randint(90, 200)
        sleep(15)
        batterylevel = 76
        
        device_data['Temperature'] = randTemperature
        device_data['Airflow'] = randAirflow
        device_data['Humidity'] = randHumidity 
        device_data['Pressure'] = randPressure
        device_data['BatteryLevel'] = batterylevel 
        
        client.publish('v1/devices/me/telemetry', json.dumps(device_data), 1)
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)