import time 
from config import *
from symbols import *


#Params:
#   sensor_status : current State
#   sp      = SensorPi object 
#   get_sensor_data : function defined the output data format
#   command_handler : function handle command from gateway
def state(sensor_status,sp,start_time,get_sensor_data,command_handler):
    # INIT
    if sensor_status == "INIT":
        sp.dataSend(NODE_MACHING,SENSOR_ID, "" )
        print("INIT: 0x13 followed with its own ID")
        packet = sp.dataReceive()
        # Listen for responses
        if packet is not None:
            # Received a packet
            if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == SENSOR_ID:
                # Received the expected ack
                sensor_status = "WORKING"
                print("INIT:0x14 followed with its own ID, entering WORKING state")

            else:
                print(f'Match Failed, received data {packet}')

    # WORKING
    if sensor_status == "WORKING":
        # Collect data
        sensor_data = get_sensor_data()
        # Send data to Gateway
        sp.dataSend(NODE_SENDING,SENSOR_ID, sensor_data )
        print("WORKING: Sensor Node collected data and sent it to gateway")
        # Listen for responses
        for i in range(MAX_TRIALS):
            packet = sp.dataReceive()
            if packet is not None:
                # Received a packet
                if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == SENSOR_ID:
                    print("WORKING: Sensor Node received a ack from gateway")
                    break


                elif packet["magic_code"] == GATWAY_COMMAND and packet["device_id"] == SENSOR_ID:
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
        sp.dataSend(NODE_ACK,SENSOR_ID, sensor_data )
        print("IDLE: Sensor Node sent ack to gateway")
        # Listen for responses

        connected = 0
        for i in range(MAX_TRIALS):
            if connected:
                break

            sp.dataSend(NODE_ACK,SENSOR_ID,"")
            packet = sp.dataReceive()
            if packet is not None:
            # Received a packet
                if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == SENSOR_ID:
                    print("IDLE: Sensor Node received a ack from gateway")
                    connected = 1
                elif packet["magic_code"] == GATWAY_COMMAND and packet["device_id"] == SENSOR_ID:
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
        sp.dataSend(NODE_MACHING,SENSOR_ID, "" )
        print("DISCONNECT: Sensor Node sent matching request to gateway")
        # Listen for responses
        packet = sp.dataReceive()
        if packet is not None:
            # Received a packet
            if packet["magic_code"] == GATWAY_ACK and packet["device_id"] == SENSOR_ID:
                # Received the expected ack
                sensor_status = "WORKING"
                print("DISCONNECT:Ack back from gateway, entering WORKING state")
                start_time = time.time()
        else:
            time.sleep(RECORD_PERIOD)
    return sensor_status
