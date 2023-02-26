# Circuit Python Code
import time
import board
from digitalio import DigitalInOut
import busio
from adafruit_rfm9x import RFM9x
import struct



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

def dataSend( mn , txData ):
    curtime = struct.pack(">f",time.time())
    data = bytes([mn,sensor_id]) + curtime + bytes(0x00) + bytes(str(txData),'ascii')
    rfm9x.send(bytearray(data))

def dataReceive():
    receive = rfm9x.receive(timeout=RECEIVE_TIMEOUT)
    if receive is not None:
        return dp.parse(receive)
    return None
        
    


# Sensor Node Behavior
while True:
    # INIT
    if sensor_status == "INIT":
        dataSend(NODE_MACHING, "" )
        print("INIT: 0x13 followed with its own ID")
        packetData = dataReceive()
        # Listen for responses
        if packetData is not None:
            # Received a packet
            print(f'{packetData["magic_code"] == bytes(GATWAY_ACK)} \n {packetData["device_id"] == bytes(sensor_id)}')
            print(f'{packetData["magic_code"]}  {GATWAY_ACK} \n {packetData["device_id"]} {bytes(sensor_id)}')
            
            if packetData["magic_code"] == GATWAY_ACK and packetData["device_id"] == sensor_id:
                # Received the expected ack
                sensor_status = "WORKING"
                print("INIT:0x14 followed with its own ID, entering WORKING state")
                start_time = time.time()
                
        else:
            print("HAHA")

    # WORKING
    if sensor_status == "WORKING":
        # Collect data
        sensor_data = get_sensor_data()
        timestep = int(time.time())
        # Send data to Gateway
        dataSend(NODE_SENDING , sensor_data)
        print("WORKING: Sensor Node collected data and sent it to gateway")
        # Listen for responses
        packet = rfm9x.receive(timeout=RECEIVE_TIMEOUT)
        if packet is not None:
            # Received a packet
            if packet[0] == GATWAY_ACK and packet[1] == sensor_id:
                # Received the expected ack
                print("WORKING: Sensor Node received a ack from gateway")
            elif packet[0] == GATWAY_COMMAND and packet[1] == sensor_id:
                print("WORKING: Sensor Node received a command from gateway")
        print(time.time() - start_time)
        if time.time() - start_time > MAX_WORKING_TIME:
                    # Maximum working time reached, enter IDLE state
                    sensor_status = "IDLE"
                    print("WORKING: Maximum working time reached, entering IDLE state")

    # IDLE
    if sensor_status == "IDLE":
        # Send ack to Gateway
        rfm9x.send(bytes([NODE_ACK, sensor_id]))
        print("IDLE: Sensor Node sent ack to gateway")
        # Listen for responses
        packet = rfm9x.receive(timeout=RECEIVE_TIMEOUT)
        if trialsCounter > MAX_TRIALS:
                sensor_status = "DISCONNECT"
                continue
        if packet is not None:
           # Received a packet
            trialsCounter = 0
            if packet[0] == GATWAY_ACK and packet[1] == sensor_id:
                # Received the expected ack
                print("IDLE: Sensor Node received a ack from gateway")
                time.sleep(4)
            elif packet[0] == GATWAY_COMMAND and packet[1] == sensor_id:
                sensor_status = command_handler()
                print("IDLE: Sensor Node received a command from gateway")
                sensor_status = "WORKING"
                print("IDLE: Ack back from gateway, entering WORKING state")
                start_time = time.time()
        else:
            trialsCounter += 1

    # DISCONNECT
    if sensor_status == "DISCONNECT":
        # Collect data
        sensor_data = get_sensor_data()
        timestep = int(time.time())
        # Send matching request to Gateway
        rfm9x.send(bytes([NODE_MACHING, sensor_id]))
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