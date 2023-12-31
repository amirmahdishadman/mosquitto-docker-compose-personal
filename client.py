import datetime
import paho.mqtt.client as mqtt
# import sqlite3
# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()
#c.execute('insert into sensors values (?,?,?)', ("msg.topic","str(msg.payload)",""))
#conn.commit()
#exit()
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code ")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    x = datetime.datetime.now()
    print(msg.topic)
    print(str(msg.payload))
    if(msg.topic == "esp32/dht/humidity"):
        humidity=float(msg.payload.decode())
    if(msg.topic == "esp32/dht/temperature"):
        temperature=float(msg.payload.decode())
    if(msg.topic == "esp32/soil/molsture"):
        molsture=float(msg.payload.decode())

        
    if(molsture>5 and humidity <20 or molsture>8):
        ret= client.publish("waterrelay","1") 
    else:
        ret= client.publish("waterrelay","0")

    if(temperature>35):
        ret= client.publish("coolerrelay","1") 

    if(temperature<15):
        ret= client.publish("heaterrelay","1")

    if(temperature>20 and temperature<30):
        ret= client.publish("coolerrelay","0")
        ret2= client.publish("heaterrelay","0")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
