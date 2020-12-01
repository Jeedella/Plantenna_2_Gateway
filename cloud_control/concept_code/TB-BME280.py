import smbus2
import bme280
import paho.mqtt.client as mqtt
import json
from time import sleep

THINGSBOARD_HOST = 'plantenna.nl'
ACCESS_TOKEN = 'qYMI8cPkKJsfwveFYi4Q'

INTERVAL = 2

sensor_data = {'temperature1': 0, 'humidity1': 0, 'pressure1': 0}

client = mqtt.Client()
# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)


client.loop_start()

port = 1
address = 0x76
bus = smbus2.SMBus(port)

while True:
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    temperature = data.temperature
    print (temperature)
    pressure = data.pressure
    humidity = data.humidity
    # Sending humidity and temperature data to ThingsBoard
    sensor_data['temperature2'] = temperature
    sensor_data['pressure2'] = pressure
    sensor_data['humidity2'] = humidity
    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    sleep(2)

client.loop_stop()
client.disconnect()

