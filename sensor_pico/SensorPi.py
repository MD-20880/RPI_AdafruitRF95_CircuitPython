import struct
from symbols import * 
import time
from config import *
from DataParser import *


RECEIVE_TIMEOUT = 2

class SensorPi:
    
    
    def __init__(self,rfm9x) -> None:
        self.rfm9x = rfm9x
        self.dataparser = DataParser()
        

    #Return Value: 0 For Success and negative for fail
    def dataSend(self, mn : int, sensor_id : int, txData : str , curtime = 0) -> int: 
        success = 0
        if curtime == 0:
            curtime = time.monotonic()
        headers = struct.pack(">bbfb",mn,sensor_id,curtime,0)
        print(headers)
        try:
            data = headers + bytes(str(txData),'ascii')
            self.rfm9x.send(bytearray(data))
        except:
            success = -1
        return success

    def dataReceive(self): 
        receive = self.rfm9x.receive(timeout=RECEIVE_TIMEOUT)
        if receive is not None:
            try:
                receiveData = self.dataparser.parse(receive)
                return receiveData
            except:
                print("Not SensorPi Format")
        return None
    