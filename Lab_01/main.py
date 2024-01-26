import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import base64
from numpy import random


#1.-----config login Ada
AIO_USERNAME = "jackwr"
AIO_KEY = "YWlvX2pwa1IyNVFXUllRZTYzRFR5T0U3RWtMY1ZDc2g="




#3.------Connect Adafruit
#Function about Adafruit
def connected ( client ) :
    print ("Ket noi thanh cong ...")
    client.subscribe( "air-conditioner" )
    client.subscribe( "led" )
    client.subscribe( "water-heater" )

def subscribe ( client , userdata , mid , granted_qos ) :
    print("Subcribe thanh cong ...", mid)
    print(userdata)

def disconnected ( client ) :
    print("Ngat ket noi ...")
    sys.exit(1)





def message ( client , feed_id , payload ):
    # ser.write(  ( str(payload) ).encode() )
    
    if (feed_id == "led"):
        if payload == "1":
            print("LED ON !!!")
        else:
            print("LED OFF #")
                
    elif (feed_id == "water-heater"):
        if payload == "1":
            print("WATER HEATER ON !!!")
        else:
            print("WATER HEATER OFF ###")

    elif (feed_id == "air-conditioner"):
        global temp_offset
        print (f"Setting Air Conditioner at {payload} ºC")
        temp_offset = float(payload) + 0.5
    else:
        print ("UNKNOWN COMMAND !!!")
        
        
        
        
        
# Connect to AdaFRUIT



def ConnectAdafruit():
    global AIO_KEY
    AIO_KEY = (base64.b64decode(AIO_KEY.encode("utf-8"))).decode("utf-8")
    client = MQTTClient ( AIO_USERNAME , AIO_KEY )
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background()
    return client


# Initialization
client_1 = ConnectAdafruit()
battery = 100
bat_offset = 0.1
temp_offset = 25




while True:
    offset = round(random.randn(),2)
    temp =  float (temp_offset + offset)
    offset = round(random.randn(),2)
    humi =  float (65 - offset)

    battery = battery - bat_offset
    if battery < 1:
        bat_offset = -0.1
    elif battery > 100:
        battery = 100
        bat_offset = 0.1
        
    
    
    
    client_1.publish("temp", temp)
    client_1.publish("humi", humi)
    client_1.publish("battery", battery)

    time.sleep(10)
