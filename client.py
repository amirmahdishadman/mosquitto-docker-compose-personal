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
        if(humidity>40):
            ret= client.publish("house/bulb1","on") 
        else:
            ret= client.publish("house/bulb1","off")
    
    if(msg.topic == "esp32/dht/temperature"):
        temperature=float(msg.payload.decode())
        if(temperature>28):
            ret= client.publish("house/bulb2","on") 
        else:
            ret= client.publish("house/bulb2","off")
    
    if(msg.topic == "esp32/soil/molsture"):
        molsture=float(msg.payload.decode())
        if(molsture>7):
            ret= client.publish("relay","1") 
        else:
            ret= client.publish("relay","0") 

    #c.execute('insert into mqtt_sensors values (?,?,?)', (msg.topic,str(msg.payload),""))
    # c.execute('insert into mqtt_sensors ("topic","value","pub_date") values (?,?,?)', (msg.topic,str(msg.payload),x))
    # conn.commit()
    #print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
