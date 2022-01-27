#!/usr/bin/env python3

import serial
import json
import time
import local_database

class Communication:
    def __init__(self, id, time, temperature, humidity, pressure, battery, airflow):
        self.id = id
        self.time = time
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.battery = battery 
        self.airflow = airflow 

def Init(): # Initialise UART link
    serialCom = serial.Serial('/dev/ttyACM0', 115200, timeout = 1) #change '/dev/ttyACM0' to name for nrf
    serialCom.reset_input_buffer()

def GetData(): # Get transmitted data and convert into dictionary
    transmitedData = serialCom.readline().decode('utf-8').rstrip()
    return transmitedData

def SendData(message):
    serialCom.write(message + "\n")

def ConvertJson(data):
    convertedVal = json.loads(data) # Dictionary conversion
    return convertedVal

def StoreData(transmitedData): # Get dictionary of gata and tramsfer it to database 
    
    if bool(transmitedData):
        latestData = Communication(transmitedData["id"], transmitedData["time"], transmitedData["temperature"], transmitedData["humidity"], transmitedData["pressure"], transmitedData["battery"], transmitedData["airflow"]) # Get dictionary data and save it into class=
        local_database.insert_data(latestData.temperature, latestData.humidity, latestData.battery, latestData.airflow, latestData.pressure, latestData.id)
        SendData("dn") # acknowledgement that data was received correctly

if __name__ == '__main__':
    Init()

    while True:

        if (serialCom.in_waiting > 0):
            data = GetData()

            if (data == "nd"):
                SendData("ok")
            else:    
                jsonData = ConvertJson(data)
                StoreData(jsonData)
        else:
            time.sleep(5) # Sleeps if there is no data to receive
                
