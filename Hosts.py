import time


class Host():
    def __init__(self, nameBytes):
        self.nameBytes = nameBytes
        self.time = time.time()


class Hosts(dict):
    def necroCheck(self):
        t = time.time()-2
        l = set()
        for k in self:
            if t > self[k].time:
                l.add(k)
        for k in l:
            print("removed:", k, self[k].nameBytes)
            self.pop(k)
    
    def addHost(self, sender, nameBytes):
        self[sender] = Host(nameBytes)
        print("register:", sender, ", hostName:", nameBytes)
        self.necroCheck()

    def writeToBuffer(self, buffer):
        self.necroCheck()
        buffer.append(len(self))
        for h in self:
            buffer += self[h].nameBytes