import board
import digitalio
import time
import busio
import digitalio
import adafruit_rfm9x
import config
import threading
import queue
import inspect


#Symbols
NODE_ACK=0x10
GATWAY_ACK=0x11
NODE_SENDING=0x12
NODE_MACHING=0x13
GATWAY_COMMAND=0x14
GATWAY_REQUEST=0x15


#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D22)
reset = digitalio.DigitalInOut(board.CE1)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)


#MCL = MAGIC_CODE_LENGTH

class DataParser:
    def __init__(self,MCL=1,DIL=1,TSL=26,PL=1):
        self.MCL = 0
        self.DIS = MCL
        self.TSS = MCL + DIL
        self.PLS = MCL + DIL + TSL
        self.DS = MCL + DIL + TSL + PL
        self.DL = 252 - self.DS
        
    def parse(self,dataLine) -> list:
        
        parseOutput = {}
        magic_code = dataLine[:self.DIS]
        device_id  = dataLine[self.DIS:self.TSS]
        timestamp = dataLine[self.TSS:self.PLS]
        page_left = dataLine[self.PLS:self.DS]
        parseOutput["magic_code"] = magic_code
        parseOutput["device_id"] = device_id
        parseOutput["timestamp"] 
        parseOutput["page_left"] = page_left
        
        return parseOutput

dp = DataParser()
        
        

#SensorList { ID : TYPE }
sensorList = {}

#Collect Data From Sensor
def Collect() -> str:
    pass 


def send() :
    rfm9x.send("ACK "+config.DEVICENAME)
    ack_back = rfm9x.receive()



def handle(data):
    id = data[1]
    if data[0] == NODE_MACHING:
        # id = int.from_bytes(data[1],"big")
        sensorList[id] = "TEMPERATURE"
        print("Ack Back to" + hex(id))
        success = rfm9x.send(bytearray([GATWAY_ACK,id]))
        print(f"Handle0x13 is {success}")
    elif data[0] == NODE_ACK:
        # id = int.from_bytes(data[1],"big")
        print("Ack Back to" + hex(id))
        success = rfm9x.send(bytearray([GATWAY_ACK,id]))
    elif data[0] == NODE_SENDING:
        #DOSOMETING
        pass
        success = rfm9x.send(bytearray([GATWAY_ACK,id]))
    
    return success


def listen(data_out:queue.Queue,dataLog:list) -> None:
    while True:
        data = rfm9x.receive(timeout=5.0)
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
    sensor_data = queue.Queue(500)
    
    
    dataLog = []
    
    
    lock  = threading.Lock()
    recevingThread = threading.Thread(None,listen,args=(sensor_data,dataLog))
    printingThread = threading.Thread(None,printing,args=(sensor_data,dataLog))
    
    recevingThread.start()
    print("Start Receving Thread")
    printingThread.start()
    print("Start Printing Thread")
    
    
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
    
    