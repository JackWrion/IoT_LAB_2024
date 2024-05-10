import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import base64

from Logger import *


# Connect to AdaFRUIT

class MQTT_Client:

    def pseudo_on_message(self, client , feed_id , payload):
        print_warning("MQTT: DO NOTHING", feed_id, payload)

    def connected (self, client):
        print_log("MQTT: CONNECTED SUCCESSFULLY !!!")
        print(client)
        

    def subscribe (self, client , userdata , mid , granted_qos ):
        print_log("MQTT: SUBSCRIBE SUCCESSFULLY > TOPIC:", self.reg_topic)


    def disconnected (self, client ) :
        print_warning("MQTT: DISCONNECTED ...")
        sys.exit(1)


    def __init__(self, username, password):
        self.client = MQTTClient ( username , password )
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.pseudo_on_message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()





    def MQTT_Subscribe(self, listofTopics):
        self.listofTopics = listofTopics

        if isinstance(listofTopics, str):
            self.reg_topic = listofTopics
            self.client.subscribe(listofTopics)
        elif isinstance(listofTopics, tuple):
            for topic in listofTopics:
                self.reg_topic = topic
                self.client.subscribe(topic)
                time.sleep(1)


    def MQTT_RegMessagesEvent(self, func):
        print_warning("MQTT: REGISTERED NEW EVENT CALLBACK !!!")
        self.client.on_message = func
    
    def MQTT_Publish(self, topic, data, cleardata = None):
        self.client.publish(topic, data)
        if cleardata:
            print_log("MQTT: PUBLISH TO",topic)
        else:
            print_log("MQTT: PUBLISH TO",topic,"=",data)





class MQTT_Sensors:
    battery = 70.0
    temp = 25
    humi = 65

    humi_offset = 0
    temp_offset = 0
    bat_offset = 0.2

    def __init__(self) -> None:
        print_log("SENSOR: INIT SUCCESSFULLY !!!")









# #----FOR TESTING ONLY ---#
# #1.-----config login Ada infomation
# AIO_USERNAME = "jackwr"
# AIO_KEY = "YWlvX2pwa1IyNVFXUllRZTYzRFR5T0U3RWtMY1ZDc2g="
# AIO_KEY = (base64.b64decode(AIO_KEY.encode("utf-8"))).decode("utf-8")

# #2.-----init client and sensors
# client_1 = MQTT_Client(AIO_USERNAME, AIO_KEY)
# client_1.MQTT_Subscribe("temp")

# mysensor = MQTT_Sensors()
# #3.-----loop processing
# turn = 0

# def myEvent(client , feed_id , payload):
#     print("TESTING NEW EVENT SUCCESSFULLY !!!")

# while True:
#     client_1.MQTT_Publish("temp",mysensor.temp)
#     if turn == 3:
#         client_1.MQTT_RegMessagesEvent(myEvent)
#     turn += 1
#     time.sleep(2)
