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

def GetTransmission(): # Get transmitted data and convert into dictionary
    transmitedData = serialCom.readline().decode('utf-8').rstrip()
    convertedVal = json.loads(transmitedData) # Dictionary conversion
    return convertedVal

def StoreData(transmitedData): # Get dictionary of gata and tramsfer it to database 
    if bool(transmitedData):
        latestData = Communication(transmitedData["id"], transmitedData["time"], transmitedData["temperature"], transmitedData["humidity"], transmitedData["pressure"], transmitedData["battery"], transmitedData["airflow"]) # Get dictionary data and save it into class=
        local_database.insert_data(latestData.temperature, latestData.humidity, latestData.battery, latestData.airflow, latestData.pressure, latestData.id)
        serialCom.write("ok\n") # acknowledgement that data was received correctly
        return 1
    else:
        serialCom.write("nok\n") # acknowledgement that data was corupted
        return 0

if __name__ == '__main__':
    Init()

    while True:
        valid = 0

        if serialCom.in_waiting > 0:

           while(not valid): # Loops data transmission untill data sent is valid
               try:
                    data = GetTransmission()
                    valid = StoreData(data)
               finally:
                    break
        else:
            time.sleep(5) # Sleeps if there is no data to receive
                
