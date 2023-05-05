# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================

#The magic code of the SensorPi protocol


#Node_Ack: Void respond to the gatway communication
NODE_ACK=0x10

#Node_Ack: Void respond to the Node communication
GATWAY_ACK=0x11

#Sending Indicator, represent the current packet is a Data packet.
NODE_SENDING=0x12

#Maching Indicator, represent the current packet is a Matching request.
NODE_MACHING=0x13

#Command Indicator, represent the current packet from GATWAY is a command, Sensor Node need to handle it with
#command_handler function in code.py
GATWAY_COMMAND=0x14
GATWAY_REQUEST=0x15
