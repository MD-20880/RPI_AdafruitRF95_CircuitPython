# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================


#This File Contains the Utilization tools for Sensor Py

from pprint import pprint


# timeConvert(basetuple, current) -> float: 
# Calculate the offset timestamp and the base timestamp, add it up to the record and calculate accurate time.
def timeConvert(basetuple, current) -> float:
    return current - basetuple[0] + basetuple[1]

def saveSensorData():
    pass

#loadSensorData(filename) -> dict: 
# This function loads sensor data from a text file
# The data in the file is expected to be in the following format:
#sensor_id:timestamp:{"sensor_reading_1":value_1,"sensor_reading_2":value_2,...}\n

def loadSensorData(filename)-> dict:
    result = {}
    data = []
    with open(filename) as f:
        data = f.readlines()

    for i in data:
        i:str
        parseLine = i.split(":")
        meta = parseLine[:2]
        contents = parseLine[2:]
        sensorcontents = ":".join(contents)[1:-2].split(",")
        contentDict = {}
        for j in range(0,len(sensorcontents)):
            content = sensorcontents[j].split(':')
            contentDict[content[0]] = content[1][1:-1]
        try:
            
            result[meta[0]][meta[1]] = contentDict
        except KeyError:
            result[meta[0]] = {}
            result[meta[0]][meta[1]] = contentDict
    
    return result


if __name__ == "__main__":
    sensordata  = loadSensorData("../log.txt")
    pprint(sensordata)
    print("DONE")