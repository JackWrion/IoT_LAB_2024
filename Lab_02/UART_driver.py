
import serial.tools.list_ports
import time
from Logger import *
import threading

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
        if ("dev/pts" in strPort) or ("COM" in strPort)  :
            splitPort = strPort.split (" ")
            commPort = ( splitPort [0])
    return commPort



def UART_ConnectPort(portName = None ):
    global ser
    
    ser = serial.Serial(portName , baudrate =115200)
    if (ser.name):
        print_log("UART CONNECTED: ",portName)

    else:
        print_warning("WARNING: UART ATTEMPTING FINDING OTHER PORTS !!!")
        portName = getPort()
        if (portName == 'None'):
            print_error("ERROR: UART NO PORT FOUND !!!")
            return
        else:
            try:
                ser = serial.Serial(portName , baudrate =115200)
                print_log("UART CONNECTED: ",portName)
            except:
                print_error("ERROR: UART BLOCKED FOUND !!!")
                return





#--- Processing Data ---#
    # Please modify how your application work in this func UART_ProcessData

def UART_ProcessData (data, sensor) :
    data = data.replace ("!", "")
    data = data.replace ("#", "")
    splitData = data.split(":")
    print(splitData)

    if splitData[1] == "temp":
        sensor.temp = float(splitData[2])
    elif splitData[1] == "humi":
        sensor.humi = float(splitData[2])
    else:
        print("WARNING: UNDEFINED FEED !!!")



mess = ""
def UART_ReadSerial(sensor):
    while True:
        bytesToRead = ser.inWaiting()
        global mess
        if (bytesToRead > 0):    
            #global mess
            mess = mess + ser.read(bytesToRead).decode("UTF-8")
            while ("#" in mess) and ("!" in mess):
                start = mess.find("!")  # 0
                end = mess.find("#")    # 4
                UART_ProcessData(mess[start:end + 1], sensor)    #0:5
                if (end == len(mess)):
                    print("end == len")
                    mess = ""
                else:
                    mess = mess[end+1:]
        
        time.sleep(1)



def UART_loop_background(sensor):
    print_warning("UART: LOOP BACKGROUND STARTING ...")
    UART_thread = threading.Thread(target=UART_ReadSerial, args=(sensor,))
    UART_thread.start()


# ---- MAIN FLOW ---- #

# ConnectPort("/dev/pts/1")
# while True:
#     readSerial(None)
#     time.sleep(1)