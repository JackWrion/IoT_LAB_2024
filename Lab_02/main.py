import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import base64
from numpy import random

from AI_driver import AI_driver

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

def disconnected ( client ) :
    print("Ngat ket noi ...")
    sys.exit(1)





def message ( client , feed_id , payload ):
    
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
battery = 70.0
bat_offset = 0.2
temp_offset = 25

sensor_turn = 0



while True:
    # Begin MAIN_FLOW    
    if sensor_turn == 0:
        offset = round(random.randn(),2)
        temp =  float (temp_offset + offset)
        client_1.publish("temp", temp)
        print("Temperature: ",temp)
        sensor_turn = 1
    
    elif sensor_turn == 1:
        offset = round(random.randn(),2)
        humi =  float (65 - offset)
        client_1.publish("humi", humi)
        print("Humidity: ",humi)
        sensor_turn = 2
    
    elif sensor_turn == 2:
        battery = round(battery - bat_offset,2)
        if battery < 1:
            bat_offset = -0.2
        elif battery > 100:
            battery = 100
            bat_offset = 0.2
        client_1.publish("battery", battery)
        print("Battery: ",battery)
        sensor_turn = 3
    
    elif sensor_turn == 3:
        data, class_name = AI_driver.AI_Execute()
        client_1.publish("camera", data)
        print("Camera detect: ", class_name)

        sensor_turn = 0

    # End MAIN_FLOW
    time.sleep(2)



AI_driver.AI_Stop()