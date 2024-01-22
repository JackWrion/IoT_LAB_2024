import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import serial.tools.list_ports
import random
import base64

ser = None


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
    client.subscribe( "bbc-led" )
    client.subscribe( "door" )


def subscribe ( client , userdata , mid , granted_qos ) :
    print("Subcribe thanh cong ...", mid)

def disconnected ( client ) :
    print("Ngat ket noi ...")
    sys.exit(1)



def message ( client , feed_id , payload ):
    # ser.write(  ( str(payload) ).encode() )
    
    if (feed_id == "bbc-led"):
        if payload == 1:
            print("LED ON !!!")
        else:
            print("LED OFF #")


    
    elif (feed_id == "door"):
        print("Change LED & FAN to ", payload, "%  !!!")

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
    client.loop_background ()


while True:
    
    offset = random.randint(-5,5)
    temp = 25 + offset
    offset = random.randint(-10,10)
    humi = 60 + offset

    client.publish("temp", temp)
    client.publish("humi", humi)

    time.sleep(5)
