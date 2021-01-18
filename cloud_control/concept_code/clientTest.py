import paho.mqtt.client as mqtt
# clients = []
# nclients = 20
clients = []
mqtt.Client.connected_flag = False
# create clients

def connectClient(clientID):
    client1 = mqtt.Client(clientID)
    clients.append(client1)
    return clients    

    # print(client)
    # print(clients)

# for i in range(nclients):
#     cname = "Client"+str(i)
#     client = mqtt.Client(cname)
#     clients.append(client)
# for client in clients:
#     client.connect("plantenna.nl")
#     client.username_pw_set("testoken1234")
#     client.loop_start()

# for client in clients: 
#     client.connect("plantenna.nl")
#     client.subscribe(topic)
#     client.publish(topic,message)

if __name__ == "__main__":
    connectClient("PA001")
    connectClient("PA002")
    connectClient("PA003")
    connectClient("PA004")
    print(clients)
    print(clients[0])