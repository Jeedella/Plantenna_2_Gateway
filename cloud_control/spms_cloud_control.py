###############################################################
# spms_cloud_control.py                                       #
# author:   Frank Arts, Omar Mhaouch                          #
# date:     November 14th, 2020                               #
# version:  1.0                                               #
#                                                             #
# version info:                                               #
# - Create functions based on functionallity of BME280.py     #
###############################################################

# import
import smbus2
import bme280
import paho.mqtt.client as mqtt
import json
from time import sleep

# global variables
THINGSBOARD_HOST = 'ec2-18-156-208-13.eu-central-1.compute.amazonaws.com'
ACCESS_TOKEN = 'zbwdc6FbMo4hsCblUvXP'

INTERVAL = 2

sensor_data = {'temperature': 0, 'humidity': 0, 'pressure': 0}

# functions
def spms_mqtt_init():
    client = mqtt.Client()
    
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)

    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)

    client.loop_start()
    
    return client

def spms_mqtt_send_data(client, temperature = 0, humidity = 0, pressure = 0):
    sensor_data['temperature'] = temperature
    sensor_data['humidity'] = humidity
    sensor_data['pressure'] = pressure
    
    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    
def spms_mqtt_stop(client):
    client.loop_stop()
    client.disconnect()

# main function
def main():
    spms_mqtt_client = spms_mqtt_init()
    
    try:
        while True:
            spms_mqtt_send_data(spms_mqtt_client)
            sleep(2)
    finally:
        spms_mqtt_stop(spms_mqtt_client)
    

if __name__ == "__main__":
    main()
	