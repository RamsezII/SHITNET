

class BufferReader():
    def __init__(self, buffer):
        self.buffer = buffer
        self.end = len(buffer)
        self.iread = 0
    
    def peekByte(self):
        return int(self.buffer[self.iread])
    
    def readByte(self):
        self.iread += 1
        return int(self.buffer[self.iread-1])
    
    def pullStringBuffer(self, pull):
        l = self.readByte()
        buf = self.buffer[self.iread:self.iread+l]
        if pull:
            self.iread += l
        return buf