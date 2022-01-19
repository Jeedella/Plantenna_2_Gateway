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

if __name__ == '__main__':
    serialCom = serial.Serial('/dev/ttyACM0', 115200, timeout = 1) #change '/dev/ttyACM0' to name for nrf
    serialCom.reset_input_buffer()

    while True:
        if serialCom.in_waiting > 0:
            transmittedData = serialCom.readline().decode('utf-8').rstrip()
            val = json.loads(transmittedData)
            
            if bool(val):
                latestData = Communication(val["id"], val["time"],val["temperature"], val["humidity"], val["pressure"], val["battery"], val["airflow"]) 
                serialCom.write("ok\n")
                local_database.insert_data(latestData.temperature, latestData.humidity, latestData.battery, latestData.airflow, latestData.pressure, latestData.id)
            else:
                serialCom.write("nok\n")
