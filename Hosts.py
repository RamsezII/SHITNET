import time

from Buffer import *
from Codes import *

class Host():
    def __init__(self, reader:BufferReader):
        self.localEnd = reader.readBytes(6)
        self.nameBytes = reader.pullString_cs()
        self.passBytes = reader.pullString_cs()
        self.time = time.time()
        print("hostName", self.nameBytes, ", publicPassword", self.passBytes)


class Hosts(dict):
    def necroCheck(self):
        t = time.time()-5
        l = set()
        for k in self:
            if t > self[k].time:
                l.add(k)
        for k in l:
            print("removed:", k, self[k].nameBytes)
            self.pop(k)
    
    def addHost(self, sender, reader:BufferReader):
        print("new endpoint", sender)
        self[sender] = Host(reader)
        self.necroCheck()
        
    def popHost(self, sender):
        if sender in self:
            pop = self.pop(sender)
            print("unregister:", sender, ", hostName:", pop.nameBytes)
        self.necroCheck()

    def writeToBuffer(self, buffer):
        self.necroCheck()
        buffer.append(len(self))
        for h in self:
            buffer += self[h].nameBytes