import paho.mqtt.client as mqtt
import sys
import json
from time import sleep

THINGSBOARD_HOST = 'plantenna.nl'
ACCESS_TOKEN = 'WH2HyLnZlQujGwaptK3e'

global mac_address1
mac_address1= {
    "device": "PA101",
    "mainCharacters":[ 
    {
        'node': "PA032", 
        'mac' : "33:11:55"
    }
]
}
# mac_address2= {'PA002': 0, 'mac' : 0}

INTERVAL = 2
global client
client = mqtt.Client()
# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

def mac_address(node, mac):
    temp = mac
    print(mac)
    # mac_address1['mac'] = "33:11"
    # mac_address1['node'] = "PA001" 
    # mac_address2['mac'] = '22:11'
    # mac_address2['PA002'] = 'PA002'
    client.publish('v1/devices/me/telemetry', json.dumps(mac_address1), 1)
    # client.publish('v1/devices/me/telemetry', json.dumps(mac_address2), 1)


if __name__ == "__main__":
    while True:
        mac_address('PA010', '33:44:55:88')
        sleep(2)
