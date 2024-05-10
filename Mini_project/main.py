import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
from numpy import random

from AI_driver import AI_driver
import UART_driver
import MQTT_driver

#1.-----config login Ada
AIO_USERNAME = "jackwr"
AIO_KEY = "aio_jpkR25QWRYQe63DTyOE7EkLc" + "VCsh"


#.------ some config parameter
USING_CAMERA = 1







def EventCallBack ( client , feed_id , payload ):
    
    if (feed_id == "led"):
        if payload == "1":
            if UART_driver.UART_WriteSerial("led", payload ):
                print("LED ON !!!")
        else:
            if UART_driver.UART_WriteSerial( "led", "0" ):
                print("LED OFF #")
                
    elif (feed_id == "water-heater"):
        if payload == "1":
            if UART_driver.UART_WriteSerial( "heater", payload ):
                print("WATER HEATER ON !!!")
        else:
            if UART_driver.UART_WriteSerial( "heater", "0" ):
                print("WATER HEATER OFF ###")

    elif (feed_id == "air-conditioner"):
        global mySensor
        if UART_driver.UART_WriteSerial("air", payload ):
            print (f"Setting Air Conditioner at {payload} ºC")
            mySensor.temp = float(payload) + 0.5
    
    elif (feed_id == "temp"):
        payload = int(payload)
        if payload >= 35:
            client.publish("air-conditioner", payload - 9)
    
    else:
        print ("UNKNOWN COMMAND !!!")
        
        
        
# Initialization        
        
# Connect to AdaFRUIT   -> init -> subsribe -> add event hanlder
client_1 = MQTT_driver.MQTT_Client(AIO_USERNAME, AIO_KEY)
client_1.MQTT_Subscribe(("led", "water-heater", "air-conditioner", "temp"))
client_1.MQTT_RegMessagesEvent(EventCallBack)


# Create Sensor: this shared sensor will be used by MAIN and UART
mySensor = MQTT_driver.MQTT_Sensors()



# UART: connect -> loop_background
UART_driver.UART_ConnectPort("COM60")
UART_driver.UART_loop_background(mySensor)




turn = 0

try:
    while True:
        # Begin MAIN_FLOW    
        # if turn == 0:                                               # random generate offset (very small decimal point) as data fluctuation
        #     offset = round(random.randn(),2)
        #     temp =  float (mySensor.temp + offset)
        #     client_1.MQTT_Publish("temp", temp)
        #     turn = 1

        # elif turn == 1:
        #     offset = round(random.randn(),2)
        #     humi =  float (mySensor.humi - offset)
        #     client_1.MQTT_Publish("humi", humi)
        #     turn = 2

                                                                    # battery gradually descreasing
        mySensor.battery = round(mySensor.battery - mySensor.bat_offset,2)
        if mySensor.battery < 1:
            mySensor.bat_offset = -0.2
        elif mySensor.battery > 100:
            mySensor.battery = 100
            mySensor.bat_offset = 0.2
        client_1.MQTT_Publish("battery", mySensor.battery)


        time.sleep(3)


        # AI processing
        class_name = "NONE"
        if USING_CAMERA:
            data, class_name = AI_driver.AI_Get()                                   # No need to processing UART, because it loop background automatically
            client_1.MQTT_Publish("camera", data, cleardata=1)
            print("Camera detect: ", class_name)
        
        
        time.sleep(2)
        
        # End MAIN_FLOW

except:
    UART_driver.UART_Stop()
    AI_driver.AI_Stop()
    sys.exit(0)