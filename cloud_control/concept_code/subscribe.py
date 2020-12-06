import paho.mqtt.client as mqtt
import json
import sys

THINGSBOARD_HOST = 'plantenna.nl'
ACCESS_TOKEN = 'qYMI8cPkKJsfwveFYi4Q'

class myData:
    data = None

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
        print("oops")
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
