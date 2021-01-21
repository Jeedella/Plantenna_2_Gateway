import projectFiles
from time import sleep

# projectFiles.init()
projectFiles.INIT()
projectFiles.init()

data = projectFiles.loadConfigData()
token1 = projectFiles.getToken("PA001", data)
token2 = projectFiles.getToken("PA002", data)

clientPA001 = projectFiles.mqttConnectDevice("PA001", token1)
clientPA002 = projectFiles.mqttConnectDevice("PA002", token2)

while True:
    projectFiles.publishData(clientPA001, 50, 10, 100, 50, 45)
    projectFiles.publishData(clientPA002, 20, 30, 50, 80, 95)
    sleep(10)

