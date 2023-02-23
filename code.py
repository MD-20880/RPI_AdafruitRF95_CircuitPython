import board
import digitalio
import time
import busio
import digitalio
import adafruit_rfm9x
import config


#Adafruit SPI INIT
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = digitalio.DigitalInOut(board.GP17)
reset = digitalio.DigitalInOut(board.GP20)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)


#LED INIT
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

#Collect Data From Sensor
def Collect() -> str:
    pass 


def send() :
    rfm9x.send("ACK "+config.DEVICENAME)
    ack_back = rfm9x.receive()


while True:
    rfm9x.send(config.DEVICENAME+":"+ config.DATATYPE) #Need to check format
    time.sleep()
    
    
