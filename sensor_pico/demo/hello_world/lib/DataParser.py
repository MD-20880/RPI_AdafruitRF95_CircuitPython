import struct
#This is a dataparser, data from sensor pi devices will be parsed by the parser.


#MCL = MAGIC_CODE_LENGTH
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
        data = struct.unpack(">bbfb",dataLine[:self.DS])
        magic_code = dataLine[:self.DIS]
        device_id  = dataLine[self.DIS:self.TSS]
        timestamp = dataLine[self.TSS:self.PLS]
        page_left = dataLine[self.PLS:self.DS]
        parseOutput["magic_code"] = data[0]
        parseOutput["device_id"] = data[1]
        parseOutput["timestamp"] = data[2]
        parseOutput["page_left"] = data[3]
        
        return parseOutput
