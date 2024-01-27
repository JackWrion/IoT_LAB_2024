import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import base64
from numpy import random


#1.-----config login Ada
AIO_USERNAME = "jackwrion12345"
AIO_KEY = "YWlvX1VoS202M3FVa0FBTmNrT2FMZUZLWkZtR0NGOVM="


#2.-----Connect Microbit
def getPort () :
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range (0 , N) :
        port = ports [ i ]
        strPort = str( port )
        if "USB-SERIAL CH340" in strPort :
            splitPort = strPort.split (" ")
            commPort = ( splitPort [0])
    return commPort

def ConnectPort():
    port = getPort()
    if (port == 'None'): return
    return serial.Serial(port , baudrate =115200)


def accessPort():
    global ser
    ser = ConnectPort()
    print('Connecting Serial: ' , ser)



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
        
        
        
    



#readSerial from Microbit --> processData --> publish to Adafruit
#Get message from Adafruit --> ser.write to Microbit



###################################################################################
######################    Send from Microbit to Gateway   #########################


# Read from Microbit

#Function about Reading process
def processData ( data ) :
    data = data.replace ("!", "")
    data = data.replace ("#", "")
    splitData = data.split(":")
    print ( splitData )
    if splitData[1] == "TEMP":
        client.publish("bbc-temp", splitData[2])


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


###################################################################################






# Connect to Ada

AIO_KEY = (base64.b64decode(AIO_KEY.encode("utf-8"))).decode("utf-8")
client = MQTTClient ( AIO_USERNAME , AIO_KEY )
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()



# API
# Open door
# Close door



def ConnectAdafruit():
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
        sensor_turn = 0
    
    

    time.sleep(5)
