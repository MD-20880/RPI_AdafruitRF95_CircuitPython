class SensorInterface:
    
    def __init__(self) -> None:
        self.activated : bool 
        self.hasReading : bool
        self.timestamp : float
        self.onreading : function
        self.onactivate : function
        self.onerror : function
        pass
    
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass