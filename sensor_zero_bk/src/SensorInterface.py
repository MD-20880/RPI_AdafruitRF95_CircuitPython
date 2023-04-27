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