import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import base64
from numpy import random

from AI_driver import AI_driver
from UART_driver import *

#1.-----config login Ada
AIO_USERNAME = "jackwr"
AIO_KEY = "YWlvX2pwa1IyNVFXUllRZTYzRFR5T0U3RWtMY1ZDc2g="
AIO_KEY = (base64.b64decode(AIO_KEY.encode("utf-8"))).decode("utf-8")
#3.------Connect Adafruit
#Function about Adafruit






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
    
    elif (feed_id == "humi"):
        global humi_offset
        print (f"Reading Humidity: {payload}%")
        humi_offset = float(payload) + 0.5
    else:
        print ("UNKNOWN COMMAND !!!")
        
        
        
        
        
# Connect to AdaFRUIT

class MQTT_Client:


    def connected (self, client):
        print("\033[32mMQTT: CONNECTED SUCCESSFULLY !!!")
        print(client)
        # self.client.subscribe( "air-conditioner" )
        # self.subscribe( "led" )
        # self.subscribe( "water-heater" )
        # self.subscribe( "humi" )



    def subscribe (self, client , userdata , mid , granted_qos ):
        print("\033[32mMQTT: SUBSCRIBE SUCCESSFULLY ---> ", self.reg_topic)


    def disconnected (self, client ) :
        print("\033[31mMQTT: DISCONNECTED ...")
        sys.exit(1)


    def __init__(self, username, password):
        self.client = MQTTClient ( username , password )
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        #self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()


    def MQTT_Subscribe(self, listofTopics):
        self.listofTopics = listofTopics

        if isinstance(listofTopics, str):
            self.reg_topic = listofTopics
            self.client.subscribe(topic)
        elif isinstance(listofTopics, tuple):
            for topic in listofTopics:
                self.reg_topic = topic
                self.client.subscribe(topic)


    def MQTT_RegisMessagesProcess(self, func):
        self.client.on_message = func
        # self.client.disconnect()
        # self.client.connect()
        # self.MQTT_Subscribe(self.listofTopics)







# Initialization

client_1 = MQTT_Client(AIO_USERNAME, AIO_KEY)


ConnectPort("/dev/pts/1")
battery = 70.0
bat_offset = 0.2
temp_offset = 25
humi_offset = 65

sensor_turn = 0



while True:
    readSerial(client=client_1)

    # Begin MAIN_FLOW    
    if sensor_turn == 0:
        offset = round(random.randn(),2)
        temp =  float (temp_offset + offset)
        client_1.publish("temp", temp)
        print("Temperature: ",temp)
        sensor_turn = 1
    
    elif sensor_turn == 1:
        offset = round(random.randn(),2)
        humi =  float (humi_offset - offset)
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