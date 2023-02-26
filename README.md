
| Index:  |
|---|
|  1.Introduction |  
|  Purpose      |  
|  requirement  | 
| Terminology   |
| 2.Notational Conventions |
| Basic Rules         |
| Protocol Parameters |





Brief Introduction:
=
This project is a purpose-based technology solution to enable low-cost, low-power, and easy-to-deploy home use wireless sensor network.

Project is based on raspberry raspberry pi series dev-boards and LoRa communication protocol. 

The initial purpose of this project is to provide a sensor module to Raspberry pi based smart home periferials. However, the project may not specific to raspberry pi and Lora communication protocol. It should be able to compatible to any platforms or communication protocols as long as the sensor could transport data in specific format.

Currently, there are plenty of research on wireless sensor network, and there are also plenty of exist instances of communication protocols. However, most of them are complex and not friendly to most of people to deal with. This issule extremely slow down the pace of massive iot device deployment.
If there exist a simple protocol that can be understood by anyone with (just a little ) electronics background. then it can encourage more iot device deployment. 

To make a protocol easy to be understood, we need to have a simple but deligent principal. (     )


What is LoRa:





Desgin Considerations:

This project is aimed to design a home use wireless sensor network. Such kind of network always has flowing properties: 
1. All sensors will be arranged with in a specific range ( Usually within 1 KM )




Home use sensor, especially sensors in hard-to-reach region should be able to last longer without any change in battery. 
According to reasons above, I choose LoRa as our communication protocol. 

According to our usage, "routing" behavior is not necessory since a single lora unit could cover almost the entire required area. Since the behavior is simple, a self defined ad-hoc network would be a better choice since it will reduce the dificulties on configuring a sensor network.   
This project defined a Network Layer transportation protocols that



Packet Design:
===


Packet Format:
=

magic number:
0x10 - NODE_ACK      Node -> Gateway    
0x11 - GATWAY_ACK    Gateway -> Node
0x12 - Sending Data  Node -> Gateway
0x13 - Maching       Node -> Gateway
0x14 - Command       Gateway -> Node
0x15 - Requesting Data Gateway -> Node

NODE_ACK=0x10
GATWAY_ACK=0x11
NODE_SENDING=0x12
NODE_MACHING=0x13
GATWAY_COMMAND=0x14
GATWAY_REQUEST=0x15



COMMUNICATION TABLE:
START WITH |    RESPOND

NODE_ACK | GATWAY_ACK
NODE_SENDING | GATWAY_ACK
GATEWAY_COMMAND | NODE_ACK
GATEWAY_REQUEST | NODE_ACK


Every data Transmission should follow format below:

MAGIC_CODE(1 Byte) | DEVICE_ID (1 Byte) | TIMESTAMP (4 Byte) | PAGE_LEFT(1 Byte) | DATA

MAGIC_CODE is 

DEVICE_ID is

TIMESTAMP is

PAGE_LEFT is

All data should be either predefined value or ascii coded string.

For Each sensor Type, We Should Set a "DEFAULT FORMAT" to that specific type. However, If you want to customize your sensor data, you should write a "DataParser" to help manage how your data look like.

Communication Process:
===

Communication can start from either side.





Data Proessing:
===

Basic Principal:
    



Sensor Types: 
    Each type of sensor will send its value to gateway through ascii encoded plain text

Sensor ID: 




Concepts:
===

    Sensor:
    Device Sensor:
    Platform Sensor: The term platform sensor refers to platform interfaces, with which the user agent interacts to obtain sensor readings for a single sensor type originated from one or more device sensors.

    Sensor Type:

    Default Sensor:



RPI Gateway Behavior:
    *Gateway* is the device that able to access and control *Sensor Nodes* belong to this *Sensor Network* 

    Gateway will collect data readings from Sensor Network and forward it to permanent storages.

    User should be able to achive following actions by accessing to a Gateway:
    1. List All Available Sensors
    2. Access Sensor Node Through its ID
    3. Access Sensor readings through its ID
    4. Setup interesting scenarios 
    5. Set Sensors to IDLE state
    6. Set Sensors to WORKING state
    


Sensor Node Behavior:
    Each sensor node have its own properties including:
        1. Sensor ID 
        2. Sensor Status

    When sensor Node start working. it will first at INIT state, at this stage, sensor node will broadcasting packet start with 0x13 followed with its own ID. At this stage, when any other LoRa devices ack it with 0x14 followed with this() sensor's ID. It will then stop broadcasting and entering WORKING state

    At WORKING stage, sensor node will continuously collect data in a default collecting frequency and send it to gateway. Each data should follow with a timestep to indicate when the data is collected. 
    At the same time, sensor will also actively receive command from gateway.
    The sensor node will automatically enter IDLE state after MAX_WORKING_TIME to save energy.


    AT IDLE state, sensor node will ack to Gateway with default every 30 second as a live check. If gateway is still online or not busying, the sensor node should receive a "Ack back" or a command from gateway.
    If nothing is received, it will start a sequence of quick acking to the gate way trying to receive "Ack back" from the gateway. When reach maximum trials, sensor will goes to DISCONNECT state. 



    AT DISCONNECT state, sensor will also collect data in a default collecting frequency, at the same time, it will constantly trying to get contact with gate way by sending Maching request.


    

    










How to Encorporate a new type of sensor into this system: 
    This project is aimed to make sensor deployment as easy as possible. In this case, we want to design a system that, if you want to deploy your own sensor , you just need to write a single file to join your own devices into this network.

    At this stage, we only provide single