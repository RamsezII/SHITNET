

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
    
    def pullStringBytes(self):
        l = self.readByte()
        buf = self.buffer[self.iread-1:self.iread+l]
        self.iread += l
        return buf


def writeIPEndToBuf(IPEnd):
    buf = bytearray()
    buf += int(IPEnd[0]).to_bytes(4, 'big')
    buf += int(IPEnd[1]).to_bytes(2, 'big')
    return buf