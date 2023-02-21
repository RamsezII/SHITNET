import time

from Buffer import *
from Codes import *


class Host():
    def __init__(self, reader:BufferReader):
        self.localEndBytes = reader.readBytes(6)
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
    
    def addHost(self, sender, reader:BufferReader, writer:bytearray):
        self.necroCheck()
        print("new endpoint", sender)
        host = Host(reader)
        if host.nameBytes in self.values():
            writer.append(Codes.alreadyHost)
        else:
            writer.append(Codes.yes)
            self[sender] = host
        
    def popHost(self, sender):
        self.necroCheck()
        if sender in self:
            pop = self.pop(sender)
            print("unregister:", sender, ", hostName:", pop.nameBytes)

    def writeToBuffer(self, buffer):
        self.necroCheck()
        buffer.append(len(self))
        for h in self:
            buffer += self[h].nameBytes