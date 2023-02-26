import board
import digitalio
import busio
import adafruit_rfm9x
import time
import threading
import struct 
from symbols import *
from config import * 
from DataParser import *
import SensorPi

### INITALIZATION ### 

#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D22)
reset = digitalio.DigitalInOut(board.CE1)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

#dataParser
dp = DataParser()    

#communication
sp = SensorPi.SensorPi(rfm9x=rfm9x)
#SensorList { ID : Sensor }
sensorList = {}

#NODE_MATCHING : Matching request from sensor node
#NODE_ACK : Ack from sensor node, need Ack back
def handle(data):
    id = data[1]
    if data[0] == NODE_MACHING:
        # id = int.from_bytes(data[1],"big")
        sensorList[id] = "TEMPERATURE"
        print("Ack Back to" + hex(id))
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
        print(f"Handle0x13 is {success}")
    elif data[0] == NODE_ACK:
        # id = int.from_bytes(data[1],"big")
        print("Ack Back to" + hex(id))
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
    elif data[0] == NODE_SENDING:
        #DOSOMETING
        pass
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
    
    return success


def listen() -> None:
    while True:
        data = sp.dataReceive()
        print(data)
        if data is not None:
            result = dp.parse(data)
            handle(data)
       
        


def printing(data_in:queue.Queue, dataLog:list) -> None:
    while True:
        # print(dataLog)
        data = data_in.get()
        # print(data)

if __name__ == "__main__":
    
    
    dataLog = []
    
    
    lock  = threading.Lock()
    recevingThread = threading.Thread(None,listen,args=(sensor_data,dataLog))

    
    recevingThread.start()
    print("Start Receving Thread")

    
    
    while True:
        # with open("log.txt","a") as f:
        #     lock.acquire()
        #     f.writelines([str(t) for t in dataLog])
        #     print("SaveDone")
        #     dataLog.clear
        #     lock.release()
        # time.sleep(5.0)
        pass
    
    
    savingThread.join()
    
    