# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================


import board
import digitalio
import busio
import adafruit_rfm9x
import time
import threading
import logging
import struct 
from symbols import *
from config import * 
from SensorInterface import *
import SensorPi
import utils


### INITALIZATION ### 
logging.basicConfig(filename='programlog.log',level=logging.INFO)

#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D22)
reset = digitalio.DigitalInOut(board.CE1)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

#dataParser 

#communication
sp = SensorPi.SensorPi(radio=rfm9x)
#SensorList { ID : Sensor }
sensorList = {}
dataList = []

#Haldel the data from another SensorPi Devices
def handle(data):
    id = data["device_id"]
    success = -1
    if data["magic_code"] == NODE_MACHING:
        # id = int.from_bytes(data[1],"big")
        sensorList[id] = Sensor(id,(data["timestamp"],time.time()))
        logging.info("Ack Back to" + str(hex(id)) + "Timestamp is ("+ str(data["timestamp"]) + "," +str(time.time())+")")
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
        logging.info(f"Handle0x13 is {success}")
    elif data["magic_code"] == NODE_ACK:
        if sensorList.get(id) is not None:
            logging.info("Ack Back to" + hex(id))
            success = sp.dataSend(GATWAY_ACK,id,"DATA")
    elif data["magic_code"] == NODE_SENDING:
        #DOSOMETING
        sensor : Sensor = sensorList[id]
        sensor.data.append(f'{data["device_id"]}:{utils.timeConvert(sensor.timestamp,data["timestamp"])}:{data["data"]}\n')
        pass
        success = sp.dataSend(GATWAY_ACK,id,"DATA")
    return success

    

#Listen to other SensorPi device communication.
def listen() -> None:
    while True:
        data = sp.dataReceive()
        if data is not None:
            logging.info("Data is " + str(data))
            success = handle(data)
            if success < 0:
                logging.info("Failed to handle, log")
       
        



if __name__ == "__main__":
    
    

    
    lock  = threading.Lock()
    recevingThread = threading.Thread(None,listen)

    
    recevingThread.start()
    logging.info("Start Receving Thread")
    

    
    
    while True:
        cmd:str = input("SensorPi >>").lower()
        args = cmd.split(" ")
        cmd = args[0]
        
        if cmd == "save":
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
                
        elif cmd == "print" or cmd == "p":
            try:
                if len(args) == 1:
                    data  = []
                    for i in sensorList.keys():
                        sensor:Sensor = sensorList[i]
                        data.extend(sensor.data)
                    for d in data[:10]:
                        print(d)
                else:
                    for d in sensorList.get(int(args[1])).data[-10:]:
                        print(d)
            except:
                print("USAGE: print[p] [SensorID]")
        elif cmd == "list":
            print(sensorList)

        elif cmd == "start":
            print(f"start")
            #TODO
        
        elif cmd == "panel":
            print("start Panel")
            #TODO
        elif cmd == "quit":
            print("Quit")
            exit(0)
        else:
            print("not a command")
        
        
        pass
    
    
    savingThread.join()
    
    