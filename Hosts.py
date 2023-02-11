import time


class Host():
    def __init__(self, nameBytes, lastTime):
        self.nameBytes = nameBytes
        self.lastTime = lastTime
    
    def necroCheck(self, t):
        return t > self.lastTime


class Hosts(dict):
    lifetime = 2
    necroChecks = False

    def addHost(self, ipEnd, nameBytes):
        self[ipEnd] = Host(nameBytes, time.time())
    
    def necroCheck(self):
        t = time.time() - Hosts.lifetime
        l = set()
        for k in self:
            if not self[k].necroCheck(t):
                l.add(k)
        for k in l:
            self.pop(k)

    def writeToBuffer(self, buffer):
        if Hosts.necroChecks:
            self.necroCheck()
        buffer[3] = len(self)
        for h in self:
            buffer += self[h].nameBytes