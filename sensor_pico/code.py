# Circuit Python Code
import time
import board
from digitalio import DigitalInOut
import busio
from adafruit_rfm9x import RFM9x
import struct
from config import *
from symbols import *
from SensorPi import *
from DataParser import *
import adafruit_mpl3115a2


#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = DigitalInOut(board.GP17)
reset = DigitalInOut(board.GP20)
rfm9x = RFM9x(spi, cs, reset, 433.0)
rfm9x.tx_power = 23
dp = DataParser()
sp = SensorPi(rfm9x=rfm9x)


i2c_pressure = busio.I2C(board.GP3,board.GP2)
pressureSensor = adafruit_mpl3115a2.MPL3115A2(i2c_pressure)

pressureSensor.sealevel_pressure = 102250



#SYMBOLS
# NODE_ACK=0x10
# GATWAY_ACK=0x11
# NODE_SENDING=0x12
# NODE_MACHING=0x13
# GATWAY_COMMAND=0x14
# GATWAY_REQUEST=0x15


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

def get_sensor_data() -> str :
    return f"PRESSURE:{pressureSensor.pressure}"



# Sensor Node Behavior
while True:
    # INIT
    if sensor_status == "INIT":
        sp.dataSend(NODE_MACHING,sensor_id, "" )
        print("INIT: 0x13 followed with its own ID")
        packet = sp.dataReceive()
        # Listen for responses
        if packet is not None:
            # Received a packet
            if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == sensor_id:
                # Received the expected ack
                sensor_status = "WORKING"
                print("INIT:0x14 followed with its own ID, entering WORKING state")
                start_time = time.time()

            else:
                print(f'Match Failed, received data {packet}')

    # WORKING
    if sensor_status == "WORKING":
        # Collect data
        sensor_data = get_sensor_data()
        # Send data to Gateway
        sp.dataSend(NODE_SENDING,sensor_id, sensor_data )
        print("WORKING: Sensor Node collected data and sent it to gateway")
        # Listen for responses
        for i in range(MAX_TRIALS):
            packet = sp.dataReceive()
            if packet is not None:
                # Received a packet
                if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == sensor_id:
                    print("WORKING: Sensor Node received a ack from gateway")
                    break


                elif packet["magic_code"] == GATWAY_COMMAND and packet["device_id"] == sensor_id:
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
        sensor_data = get_sensor_data()
        sp.dataSend(NODE_ACK,sensor_id, sensor_data )
        print("IDLE: Sensor Node sent ack to gateway")
        # Listen for responses

        connected = 0
        for i in range(MAX_TRIALS):
            if connected:
                break

            sp.dataSend(NODE_ACK,sensor_id,"")
            packet = sp.dataReceive()
            if packet is not None:
            # Received a packet
                if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == sensor_id:
                    print("IDLE: Sensor Node received a ack from gateway")
                    connected = 1
                elif packet["magic_code"] == GATWAY_COMMAND and packet["device_id"] == sensor_id:
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
        sp.dataSend(NODE_MACHING,sensor_id, "" )
        print("DISCONNECT: Sensor Node sent matching request to gateway")
        # Listen for responses
        packet = sp.dataReceive()
        if packet is not None:
            # Received a packet
            if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == sensor_id:
                # Received the expected ack
                sensor_status = "WORKING"
                print("DISCONNECT:Ack back from gateway, entering WORKING state")
                start_time = time.time()
        else:
            time.sleep(RECORD_PERIOD)


