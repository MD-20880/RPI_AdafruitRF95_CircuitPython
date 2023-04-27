# Circuit Python Code
import time
import busio
import board
from digitalio import DigitalInOut

from __SensorPi import *
from adafruit_rfm9x import RFM9x


#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = DigitalInOut(board.GP5)
reset = DigitalInOut(board.GP0)
rfm9x = RFM9x(spi, cs, reset, 433.0)
rfm9x.tx_power = 23
dp = DataParser()
sp = SensorPi(rfm9x=rfm9x)

# User Define Functions
def command_handler(cmd):
    return 0

def get_sensor_data() -> str :
    return "Hello_World"


# Sensor Node Behavior
sensor_status = "INIT"
start_time = time.time()
while True:
    sensor_status = state(sensor_status,sp,start_time,get_sensor_data,command_handler)

