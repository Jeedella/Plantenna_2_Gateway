import sys
from mqttConnect import *
from publishData import *


def initialize():
    INIT()
    init()

def connectDevices():
    configData = loadConfigData()
    # print(token)
    mqttConnectDevice(getToken("PA001", configData))
    mqttConnectDevice(getToken("PA002", configData))
    mqttConnectDevice(getToken("PA003", configData))
    mqttConnectDevice(getToken("PA004", configData))
    mqttConnectDevice(getToken("PA005", configData))
    
def main():
    initialize()
    connectDevices()

if __name__ == "__main__":
    main()
