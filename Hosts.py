import time


class Host():
    def __init__(self, nameBytes, passBytes):
        self.nameBytes = nameBytes
        self.passBytes = passBytes
        self.time = time.time()


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
    
    def addHost(self, sender, nameBytes, passBytes):
        if sender not in self:
            print("register:", sender, ", hostName:", nameBytes, ", pass1:", passBytes)
        self[sender] = Host(nameBytes, passBytes)
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