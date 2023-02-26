import struct
from symbols import * 


class SensorPi:
    
    
    def __init__(self,rfm9x) -> None:
        self.rfm9x = rfm9x
        


    def dataSend(self, sensor_id, mn, txData ):
        curtime = struct.pack(">f",time.time())
        data = bytes([mn,sensor_id]) + curtime + bytes(0x00) + bytes(str(txData),'ascii')
        self.rfm9x.send(bytearray(data))

    def dataReceive(self):
        receive = self.rfm9x.receive(timeout=RECEIVE_TIMEOUT)
        if receive is not None:
            return receive
        return None
        
    