# Author: Omar Mhaouch
# Date: 26-01-2021
# Last updated: 27-01-2021

# This script is used to send incoming data from the NRF to the cloud. 
# This is the main script which should be runned.


from projectFiles import *
from time import sleep
import random
# Initialize dictionary to save the clients

# Initialize
INIT()
init()

# load the data from the config file
data = loadConfigData()

# Create a MQTT connection with the devices provided
def conDevice(nodeName):   
    mqttClient = clientName(nodeName)
    mqttToken = getToken(nodeName, data)
    mqttValue = mqttConnectDevice(mqttClient, mqttToken)
    clients[nodeName] = mqttValue
    return

# Publish the data coming from the NRF's
def pubData(clientValue, t, h, p, a, b):
    client = clients.get(clientValue)
    publishData(client, t, h, p, a, b)

# Create the connection
conDevice("PA001")
conDevice("PA002")



while True:
    # Generate random data to simulate the function
    randTemperature = random.randint(18, 25)
    randPressure = random.uniform(0.5, 1.5)
    randHumidity = random.randint(30, 50)
    randAirflow = random.randint(90, 200)

    # Publish the random generated data 
    pubData("PA001", randTemperature, randHumidity, randPressure, randAirflow, 35 )
    pubData("PA002", randTemperature, randHumidity, randPressure, randAirflow, 35)
    sleep(5)

