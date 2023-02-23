class SensorInterface:
    
    def __init__(self) -> None:
        self.activated
        self.hasReading
        self.timestamp
        self.onreading
        self.onactivate
        self.onerror
        pass
    
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass