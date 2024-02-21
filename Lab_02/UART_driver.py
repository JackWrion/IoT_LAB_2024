
import serial.tools.list_ports
import time



#--- INITIAL PORT ---#

# global serialPort
ser = None




# Return portName if found any port
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range (0 , N) :
        port = ports [ i ]
        strPort = str( port )
        if "dev/pts" in strPort :
            splitPort = strPort.split (" ")
            commPort = ( splitPort [0])
    return commPort



def ConnectPort(portName = None ):
    global ser
    
    ser = serial.Serial(portName , baudrate =115200)
    if (ser.name):
        print("UART CONNECTED: ",portName)

    else:
        print("WARNING: UART ATTEMPTING FINDING OTHER PORTS !!!")
        portName = getPort()
        if (portName == 'None'):
            print("ERROR: UART NO PORT FOUND !!!")
            return
        else:
            try:
                ser = serial.Serial(portName , baudrate =115200)
                print("UART CONNECTED: ",portName)
            except:
                print("ERROR: UART BLOCKED FOUND !!!")
                return




#--- Processing Data ---#


def processData (client,  data) :
    data = data.replace ("!", "")
    data = data.replace ("#", "")
    splitData = data.split(":")
    print ( splitData )

    if splitData[1] == "temp":
        client.publish("air-conditioner", splitData[2])
    elif splitData[1] == "humi":
        client.publish("humi", splitData[2])
    else:
        print("WARNING: UNDEFINED FEED !!!")


mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    global mess

    if (bytesToRead > 0):    
        #global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")  # 0
            end = mess.find("#")    # 4
            processData(client, mess[start:end + 1])    #0:5
            if (end == len(mess)):
                print("end == len")
                mess = ""
            else:
                mess = mess[end+1:]




# ---- MAIN FLOW ---- #

# ConnectPort("/dev/pts/1")
# while True:
#     readSerial(None)
#     time.sleep(1)