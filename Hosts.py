import time


class Host():

    def __init__(self, nameBytes, lifeTime):
        self.nameBytes = nameBytes
        self.lifeTime = lifeTime
        if lifeTime > 0:
            self.lifeTime += time.time()
    
    def necroCheck(self, t):
        return t > self.lifeTime


class Hosts(dict):

    def necroCheck(self):
        t = time.time()
        l = set()
        for k in self:
            if self[k].necroCheck(t):
                l.add(k)
        for k in l:
            print("removed:", k, self[k].nameBytes)
            self.pop(k)

    def writeToBuffer(self, buffer):
        self.necroCheck()
        buffer[3] = len(self)
        for h in self:
            buffer += self[h].nameBytes