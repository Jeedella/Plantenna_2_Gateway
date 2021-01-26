import projectFiles
from time import sleep
import random

# projectFiles.init()
projectFiles.INIT()
projectFiles.init()

data = projectFiles.loadConfigData()
token1 = projectFiles.getToken("PA001", data)
token2 = projectFiles.getToken("PA002", data)
token3 = projectFiles.getToken("PA003", data)
token4 = projectFiles.getToken("PA004", data)
token5 = projectFiles.getToken("PA005", data)
token6 = projectFiles.getToken("PA006", data)
token7 = projectFiles.getToken("PA007", data)

clientPA001 = projectFiles.mqttConnectDevice("PA001", token1)
clientPA002 = projectFiles.mqttConnectDevice("PA002", token2)
clientPA003 = projectFiles.mqttConnectDevice("PA003", token3)
clientPA004 = projectFiles.mqttConnectDevice("PA004", token4)
clientPA005 = projectFiles.mqttConnectDevice("PA005", token5)
clientPA006 = projectFiles.mqttConnectDevice("PA006", token6)
clientPA007 = projectFiles.mqttConnectDevice("PA007", token7)


while True:

    randTemperature = random.randint(18, 25)
    randPressure = random.uniform(0.5, 1.5)
    randHumidity = random.randint(30, 50)
    randAirflow = random.randint(90, 200)
     
    projectFiles.publishData(clientPA001, randTemperature, randHumidity, randPressure, randAirflow, 35)
    projectFiles.publishData(clientPA002, randTemperature, randHumidity, randPressure, randAirflow, 45)
    projectFiles.publishData(clientPA003, randTemperature, randHumidity, randPressure, randAirflow, 55)
    projectFiles.publishData(clientPA004, randTemperature, randHumidity, randPressure, randAirflow, 65)
    projectFiles.publishData(clientPA005, randTemperature, randHumidity, randPressure, randAirflow, 75)
    projectFiles.publishData(clientPA006, randTemperature, randHumidity, randPressure, randAirflow, 85)
    projectFiles.publishData(clientPA007, randTemperature, randHumidity, randPressure, randAirflow, 95)
    sleep(15)

