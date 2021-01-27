# Author: Omar Mhaouch
# Date: 27-01-2021
# Last updated: 27-01-2021

# This script is used to listen for messages coming from the dashboard
# The subscribe method from MQTT is used to manage this.
global clients
clients = {}

import paho.mqtt.client as mqtt
import json
# from ..main import clients

def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')

def on_message(client, userdata, msg):
    # print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # # Decode JSON request
    # print(client)
    key_list = list(clients.keys())
    val_list = list(clients.values())
    
    position = val_list.index(client)
    device = key_list[position]
    data = json.loads(msg.payload)
    
    if data['params'] == 'reset':
        print("I want the NRF to reset!, coming from", device)
    elif data['params'] == 'restart':
        print("I want the NRF to restart!, coming from", device)
    elif data['params'] == 'shutdown':
        print("I want the NRF to shutdown, coming from", device)
    else:
        print("Something went wrong, coming from", device)

