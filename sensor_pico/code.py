# Circuit Python Code
import time
import board
from digitalio import DigitalInOut,Direction
import busio
from adafruit_rfm9x import RFM9x
import struct
import adafruit_mpl3115a2
from __SensorPi import *


#Adafruit SPI INIT
#GP18 SCK  GP19 TX(MOSI)  GP16 RX(MISO)
spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = DigitalInOut(board.GP5)
reset = DigitalInOut(board.GP0)
rfm9x = RFM9x(spi, cs, reset, 433.0)
rfm9x.tx_power = 23
dp = DataParser()
sp = SensorPi(rfm9x=rfm9x)


 #Sensors INIT
try:   
    i2c_pressure = busio.I2C(board.GP15,board.GP14)
    pressureSensor = adafruit_mpl3115a2.MPL3115A2(i2c_pressure)
    pressureSensor.sealevel_pressure = 102250
    print("Sensor Detected")
except:
    print("NO SENSOR DETECTED, DEBUG")

#PERIPHALS INIT
led = DigitalInOut(board.GP13)
led.direction = Direction.OUTPUT
pir = DigitalInOut(board.GP17)
pir.direction = Direction.INPUT



#SENSOR NODE COMMAND HANDLER
def command_handler(cmd):
    if cmd == "Open":
        led.value = 1
    if cmd == "Close":
        led.value = 0
    return 0



#Sensor Data Format
def get_sensor_data() -> str :
    try:
        return "[PRESSURE:{"+str(pressureSensor.pressure)+"},PIR:{"+ ("1" if pir.value else "0") +"},TEMPERATURE:{"+str(pressureSensor.temperature)+"}]"
    except:
        return "DEBUG"




#Main Process
sensor_status = "INIT"
start_time = time.time()W
while True:
    sensor_status = state(sensor_status,sp,start_time,get_sensor_data,command_handler)

