import struct


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
        magic_code = dataLine[:self.DIS]
        device_id  = dataLine[self.DIS:self.TSS]
        timestamp = dataLine[self.TSS:self.PLS]
        page_left = dataLine[self.PLS:self.DS]
        parseOutput["magic_code"] = int.from_bytes(magic_code,"big")
        parseOutput["device_id"] = int.from_bytes(device_id,"big")
        parseOutput["timestamp"] = struct.unpack(">f",timestamp)
        parseOutput["page_left"] = int.from_bytes(page_left,"big")
        
        return parseOutput
