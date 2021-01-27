# Author: Omar Mhaouch
# Date: 26-01-2021
# Last updated: 26-01-2021

# This script is used to handle incoming messages from the cloud.
# These are controls which are needed from the user.

import paho.mqtt.client as mqtt
import json
import sys
from time import sleep

# Initialize the dashboard variables
THINGSBOARD_HOST = 'plantenna.nl'
ACCESS_TOKEN = '2P0YswIskauBVegsjRR3'


class myData:
    data = None

# Initialize the MQTT connection
def init():
    global client
    client = mqtt.Client()

    client.username_pw_set(ACCESS_TOKEN)
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)

    # Register connect callback
    client.on_connect = on_connect
    # Registed publish message callback
    client.on_message = on_message
    # Set access token
    client.loop_forever()
    return client

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # # Decode JSON request
    data = json.loads(msg.payload)
    if data['params'] == 'reset':
        print("I want a reset!")
    elif data['params'] == 'restart':
        print("I want a restart!")
    else:
        print("Something went wrong")
    data = myData()

def main():
        try:
            init()
            while True:
                print(myData)
                sleep(2)
        finally:
            print("exiting program")
if __name__ == "__main__":
    main()
