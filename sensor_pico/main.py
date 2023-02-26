# Circuit Python Code
import time
import board
from digitalio import DigitalInOut
import busio
from adafruit_rfm9x import RFM9x
import struct

class SensorPi:
    
    
    def __init__(self,rfm9x) -> None:
        self.rfm9x = rfm9x
        


    def dataSend(self, sensor_id, mn, txData):
        curtime = struct.pack(">f",time.time())
        data = bytes([mn,sensor_id]) + curtime + bytes(0x00) + bytes(str(txData),'ascii')
        self.rfm9x.send(bytearray(data))

    def dataReceive(self):
        receive = self.rfm9x.receive(timeout=RECEIVE_TIMEOUT)
        if receive is not None:
            return receive
        return None

class DataParser:
    def __init__(self,MCL=1,DIL=1,TSL=4,PL=1):
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
        parseOutput["magic_code"] = int.from_bytes(magic_code,"big")
        parseOutput["device_id"] = int.from_bytes(device_id,"big")
        parseOutput["timestamp"] = struct.unpack(">f",timestamp)
        parseOutput["page_left"] = int.from_bytes(page_left,"big")
        
        return parseOutput


# Configure the radio
#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = DigitalInOut(board.GP17)
reset = DigitalInOut(board.GP20)
rfm9x = RFM9x(spi, cs, reset, 433.0)
rfm9x.tx_power = 23
dp = DataParser()
sp = SensorPi(rfm9x=rfm9x)




#SYMBOLS
NODE_ACK=0x10
GATWAY_ACK=0x11
NODE_SENDING=0x12
NODE_MACHING=0x13
GATWAY_COMMAND=0x14
GATWAY_REQUEST=0x15


# Sensor Node Properties
sensor_id = 0x12
sensor_status = "INIT"
MAX_WORKING_TIME = 10
RECEIVE_TIMEOUT = 2
MAX_TRIALS = 2
RECORD_PERIOD = 5
trialsCounter = 0

def command_handler():
    return 0

def get_sensor_data():
    return 20


# Sensor Node Behavior
while True:
    # INIT
    if sensor_status == "INIT":
        sp.dataSend(NODE_MACHING, "" )
        print("INIT: 0x13 followed with its own ID")
        packet = sp.dataReceive()
        # Listen for responses
        if packet is not None:
            try:
                packetData = dp.parse()
            except Exception:
                continue
            # Received a packet
            if packetData["magic_code"] == GATWAY_ACK and packetData["device_id"] == sensor_id:
                # Received the expected ack
                sensor_status = "WORKING"
                print("INIT:0x14 followed with its own ID, entering WORKING state")
                start_time = time.time()
                
        else:
            print("Match Failed")

    # WORKING
    if sensor_status == "WORKING":
        # Collect data
        sensor_data = get_sensor_data()
        # Send data to Gateway
        sp.dataSend(NODE_SENDING , sensor_data)
        print("WORKING: Sensor Node collected data and sent it to gateway")
        # Listen for responses
        for i in range(MAX_TRIALS):
            packet = sp.dataReceive()
            if packet is not None:
                # Received a packet
                if packet[0] == GATWAY_ACK and packet[1] == sensor_id:
                    print("WORKING: Sensor Node received a ack from gateway")
                    break
                
                
                elif packet[0] == GATWAY_COMMAND and packet[1] == sensor_id:
                    print("WORKING: Sensor Node received a command from gateway")
                    break
                    
                    
        print(time.time() - start_time)
        if time.time() - start_time > MAX_WORKING_TIME:
                    # Maximum working time reached, enter IDLE state
                    sensor_status = "IDLE"
                    print("WORKING: Maximum working time reached, entering IDLE state")

    # IDLE
    if sensor_status == "IDLE":
        # Send ack to Gateway
        sp.dataSend(sensor_id,NODE_ACK,"")
        print("IDLE: Sensor Node sent ack to gateway")
        # Listen for responses
        
        connected = 0
        for i in range(MAX_TRIALS):
            if connected:
                break
            
            
            packet = sp.dataReceive()
            if packet is not None:
            # Received a packet
                if packet[0] == GATWAY_ACK and packet[1] == sensor_id:
                    print("IDLE: Sensor Node received a ack from gateway")
                    connected = 1
                elif packet[0] == GATWAY_COMMAND and packet[1] == sensor_id:
                    connected = 1
                    sensor_status = command_handler()
                    print("IDLE: Sensor Node received a command from gateway")
                    sensor_status = "WORKING"
                    print("IDLE: Ack back from gateway, entering WORKING state")
                    start_time = time.time()
                    

        if not connected:
            sensor_status = "DISCONNECT"
        else:
            time.sleep(RECORD_PERIOD)
        
        
        
    # Potential Security Issues exist, need expand
    # DISCONNECT
    if sensor_status == "DISCONNECT":
        # Collect data
        sensor_data = get_sensor_data()
        # Send matching request to Gateway
        sp.dataSend(sensor_id,NODE_MACHING,"")
        print("DISCONNECT: Sensor Node sent matching request to gateway")
        # Listen for responses
        packet = rfm9x.receive(timeout=RECEIVE_TIMEOUT)
        if packet is not None:
            # Received a packet
            if packet[0] == GATWAY_ACK and packet[1] == sensor_id:
                # Received the expected ack
                sensor_status = "WORKING"
                print("DISCONNECT:Ack back from gateway, entering WORKING state")
                start_time = time.time()
        else:
            time.sleep(RECORD_PERIOD)