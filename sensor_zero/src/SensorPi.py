# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================


import struct
from symbols import * 
import time
from config import *
from DataParser import *


RECEIVE_TIMEOUT = 2


#The SensorPi is a class containing information about a sensor node. 
#The structure of Sensor Pi object should reflect the functionality of the sensor node
#After Reading the implementation structure of a SensorPi class,
# Users need to be able to answer questions like "What Could we get from this sensor Node" and
#"What consist of this sensor Node"
#

#{
# When desinging this file, I was trying to create a skeleton for each sensor nodes 
# Sensor Nodes with different implementations could be easily adapted to this system by 
# Implementing this class. 
# 
# here, the self.rfm9x is better changed to self.radio
#    self.rfm9x -> self.radio
#    This part of the code is trying to add variety to the system.
#    With this implemented, the host could automatically check the availability of the communication radio
# }


class SensorPi:
    
                                                            
    def __init__(self,radio) -> None:
        self.radio = radio
        self.dataparser = DataParser()
        self.sensorList = {}
        self.dataList = []
        

    #Return Value: 0 For Success and negative for fail
    def dataSend(self, mn : int, sensor_id : int, txData : str , curtime = 0) -> int: 
        success = 0
        if curtime == 0:
            curtime = time.monotonic()
        headers = struct.pack(">bbfb",mn,sensor_id,curtime,0)
        try:
            data = headers + bytes(str(txData),'ascii')
            self.radio.send(bytearray(data))
        except:
            success = -1
        return success

    def dataReceive(self): 
        receive = self.radio.receive(timeout=RECEIVE_TIMEOUT)
        if receive is not None:
            try:
                receiveData = self.dataparser.parse(receive)
                return receiveData
            except:
                # print("Not SensorPi Format")
                pass
        return None
    

    