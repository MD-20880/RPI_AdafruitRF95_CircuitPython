# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================


#This file is designed to describe the basic data of a sensor.
#Before using the sensor in the system, sensors should register themself to the system by 
# implementing the Sensor Interface. With the Sensor Interface, the host could 
#1. Know the type of the sensor
#2. get the basic information of the data.
 
#This file might could combine with SensorPi.py

class SensorInterface:
    
    def __init__(self) -> None:
        self.timestamp : tuple = None
        self.lastFire : float = None
        self.description : str = "UNKNOWN"
        self.id : int
        self.data = []
        pass
    
    
    def start(self) -> None:
        print("Start Sensor")
    
    def stop(self) -> None:
        print("Stop Sensor")
    
    
class Sensor(SensorInterface):
    def __init__(self,id,timestamp) -> None:
        super().__init__()
        self.id = id
        self.timestamp = timestamp
        if self.timestamp == None or type(timestamp[0]) is not float or type(timestamp[1]) is not float  :  
            raise Exception(f" INIT TIMESTAMP FAILED. Received Type {type(timestamp)}")
           
    
    def start(self) -> None:
        return super().start()
    
    def stop(self) -> None:
        return super().stop()