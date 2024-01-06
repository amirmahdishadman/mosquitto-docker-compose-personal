import datetime
import paho.mqtt.client as mqtt
from datetime import datetime
import time
# import sqlite3
# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()
#c.execute('insert into sensors values (?,?,?)', ("msg.topic","str(msg.payload)",""))
#conn.commit()
#exit()
# The callback for when the client receives a CONNACK response from the server.
humidit=0
temperature=0
molsture=0
light_sensor=0
light=0
heater=0
water=0
coller=0
day=0
night=0
time_difference_in_minutes=0

def turn_light_on(difference_in_seconds,clinet):
    global humidity
    global temperature
    global molsture
    global light_sensor
    global light
    global heater
    global water
    global coller
    global day
    global night
    global time_difference_in_minutes

    ret= client.publish("light","1")
    light=1
    time.sleep(difference_in_seconds)
    ret= client.publish("light","0")
    light=0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code ")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global humidity
    global temperature
    global molsture
    global light_sensor
    global light
    global heater
    global water
    global coller
    global day
    global night
    global time_difference_in_minutes
    x = datetime.datetime.now()
    print(msg.topic)
    print(str(msg.payload))
    if(msg.topic == "esp32/dht/humidity"):
        humidity=float(msg.payload.decode())
    if(msg.topic == "esp32/dht/temperature"):
        temperature=float(msg.payload.decode())
    if(msg.topic == "esp32/soil/molsture"):
        molsture=float(msg.payload.decode())
    if(msg.topic == "esp32/light"):
        light_sensor=float(msg.payload.decode())

    
    if((molsture>7 and humidity <20 or molsture>8) and water==0):
        ret= client.publish("waterrelay","1")
        water=1

    if(molsture<6 and water == 1):
        ret= client.publish("waterrelay","0")
        water=0

    if(temperature>35 and coller==0):
        ret= client.publish("coolerrelay","1") 
        coller=1

    if(temperature<15 and heater==0):
        ret= client.publish("heaterrelay","1")
        heater=1

    if(temperature>20 and temperature<30 and (heater==1 or coller==1)):
        ret= client.publish("coolerrelay","0")
        ret2= client.publish("heaterrelay","0")

    light_lenth=10
    if(light_sensor<5 and light ==0):
        night = datetime.now()
        time_difference = night -day
        if(time_difference.total_seconds()>0 and time_difference.total_seconds()<light_lenth):
            turn_light_on(light_lenth-time_difference.total_seconds(),client)

    if(light_sensor>5 and light==1):
        day = datetime.now()
        ret= client.publish("light","0")
        light=0





client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
