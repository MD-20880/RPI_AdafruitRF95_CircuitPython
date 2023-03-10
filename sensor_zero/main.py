import board
import digitalio
import busio
import adafruit_rfm9x
import time
import threading
import struct 
from symbols import *
from config import * 
from SensorInterface import *
import SensorPi
import logging
import utils

### INITALIZATION ### 

#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D22)
reset = digitalio.DigitalInOut(board.CE1)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

#dataParser 

#communication
sp = SensorPi.SensorPi(rfm9x=rfm9x)
#SensorList { ID : Sensor }
sensorList = {}
dataList = []

#NODE_MATCHING : Matching request from sensor node
#NODE_ACK : Ack from sensor node, need Ack back
def handle(data):
    id = data["device_id"]
    success = -1
    if data["magic_code"] == NODE_MACHING:
        # id = int.from_bytes(data[1],"big")
        sensorList[id] = Sensor(id,(data["timestamp"],time.time()))
        print("Ack Back to" + hex(id))
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
        print(f"Handle0x13 is {success}")
    elif data["magic_code"] == NODE_ACK:
        # id = int.from_bytes(data[1],"big")
        print("Ack Back to" + hex(id))
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
    elif data["magic_code"] == NODE_SENDING:
        #DOSOMETING
        sensor : Sensor = sensorList[id]
        sensor.data.append(f'{data["device_id"]}:{utils.timeConvert(sensor.timestamp,data["timestamp"])}:{data["data"]}\n')
        pass
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
    
    return success


def listen() -> None:
    while True:
        data = sp.dataReceive()
        if data is not None:
            print("Data is " + str(data))
            success = handle(data)
            if success < 0:
                print("Failed to handle, log")
       
        


if __name__ == "__main__":
    
    

    
    lock  = threading.Lock()
    recevingThread = threading.Thread(None,listen)

    
    recevingThread.start()
    print("Start Receving Thread")

    
    
    while True:
        data  = []
        for i in sensorList.keys():
            sensor:Sensor = sensorList[i]
            data.extend(sensor.data)
            sensorList[i].data = []
        with open("log.txt","a") as f:
            lock.acquire()
            f.writelines(data)
            print("SaveDone")
            lock.release()
        time.sleep(5.0)
        pass
    
    
    savingThread.join()
    
    