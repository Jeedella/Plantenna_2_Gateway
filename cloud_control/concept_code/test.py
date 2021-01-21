import paho.mqtt.client as mqtt
import json
import random
from time import sleep

# dashboard host location
THINGSBOARD_HOST = 'plantenna.nl'

# access tokens of different devices
PA001 = '2P0YswIskauBVegsjRR3'
PA002 = 'RvntQNB8WjacLMUTxEJY'
PA003 = 'ERdwkf3Oi5KgVsIDCMpN'

#initial data 
sensor_data = {'Temperature': 0, 'Humidity': 0, 'Pressure': 0}

#initiate the connections with the diffferent clients
clientPA001 = mqtt.Client()
clientPA001.username_pw_set(PA001)
clientPA001.connect(THINGSBOARD_HOST, 1883, 60)
clientPA001.loop_start()

# clientPA002 = mqtt.Client()
# clientPA002.username_pw_set(PA002)
# clientPA002.connect(THINGSBOARD_HOST, 1883, 60)
# clientPA002.loop_start()

# clientPA003 = mqtt.Client()
# clientPA003.username_pw_set(PA003)
# clientPA003.connect(THINGSBOARD_HOST, 1883, 60)
# clientPA003.loop_start()

while True:
    randTemperature = random.randint(18, 25)
    randPressure = random.uniform(0.5, 1.5)
    randHumidity = random.randint(30, 50)
    # randAirflow = random.randint(90, 200)
    sleep(15)
    # batterylevel = 76
    
    sensor_data['Temperature'] = randTemperature
    # device_data['Airflow'] = randAirflow
    sensor_data['Humidity'] = randHumidity 
    sensor_data['Pressure'] = randPressure
    # device_data['BatteryLevel'] = batterylevel 
    
    clientPA001.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    # clientPA002.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    # clientPA003.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    sleep(1)

clientPA001.loop_stop()
# clientPA002.loop_stop()
# clientPA003.loop_stop()

clientPA001.disconnect()
# clientPA002.disconnect()
# clientPA003.disconnect()