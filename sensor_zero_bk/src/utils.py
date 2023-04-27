# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================


from pprint import pprint

def timeConvert(basetuple, current) -> float:
    return current - basetuple[0] + basetuple[1]

def saveSensorData():
    pass

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