###############################################################
# spms_cloud_control.py                                       #
# author:   Frank Arts, Omar Mhaouch, Reynaldo Dirksen        #
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
THINGSBOARD_HOST = 'plantenna.nl'
ACCESS_TOKEN = 'h2WcsjGlrQrbhsQcnzGU'

INTERVAL = 2

sensor_data = {'temperature': 0, 'humidity': 0, 'pressure': 0, 'batteryVoltage': 0, 'airflow': 0, 'date' : 0 , 'time': 0}

# functions
def spms_mqtt_init():
    client = mqtt.Client()
    
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)

    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    try:
        (client.connect(THINGSBOARD_HOST, 1883, 60))
    except:
        return False

    (client.loop_start())
    
    return client

def spms_mqtt_send_data(client, temperature , humidity , pressure, batV, airflow, date, time):
    sensor_data['temperature'] = temperature
    sensor_data['humidity'] = humidity
    sensor_data['pressure'] = pressure
    sensor_data['batteryVoltage'] = batV
    sensor_data['airflow'] = airflow
    sensor_data['date'] = date
    sensor_data['time'] = time
    
    while(1):
        try:
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        finally:
            break
        
def spms_mqtt_stop(client):
    client.loop_stop()
    client.disconnect()

# main function
def main():
    spms_mqtt_client = spms_mqtt_init()
    
    
    try:
        while True:
            spms_mqtt_send_data(spms_mqtt_client, 0, 0, 0, 0, 0, 0, 0)
            sleep(2)
    finally:
        spms_mqtt_stop(spms_mqtt_client)
    

if __name__ == "__main__":
    main()
	
