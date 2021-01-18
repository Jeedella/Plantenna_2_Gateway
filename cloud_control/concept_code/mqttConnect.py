import paho.mqtt.client as mqtt
import json
from time import sleep

def INIT():

    global THINGSBOARD_HOST 
    THINGSBOARD_HOST = 'plantenna.nl'

    INTERVAL = 2
    return


def loadConfigData():    
    try:
        with open("config.json", 'r') as config_file:
            data = json.load(config_file)
        return data
    except Exception as e:
        print(f'Could not load config file, {e}')

def getToken(deviceName, configData):
    try:
        token = configData[deviceName]['ACCESSTOKEN']
        print(token)
        return token
    except Exception as e:
        print(f'could not retrieve access token, {e}')
        
def mqttConnectDevice(token):
    client = mqtt.Client()
    client.username_pw_set(token)
    client.connect("plantenna.nl", 1883, 60)
    client.loop_start()
    return client
    

def mqttCloseConnection(client):
    client.loop_stop()
    client.disconnect()

# def main():
#     INIT()
#     loadConfigData()  

if __name__ == "__main__":
    print("MQTT publish test file")
    INIT()
    data = loadConfigData()
    token = getToken("PA002", data)
    client = mqttConnectDevice(token)
    mqttCloseConnection(client)