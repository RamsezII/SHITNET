

import ipaddress


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
    
    def pullString_cs(self):
        l = self.readByte()
        buf = self.buffer[self.iread-1:self.iread+l]
        self.iread += l
        return buf


def writeIPEndToBuf(IPEnd):
    buf = bytearray()
    buf += int(ipaddress.ip_address(IPEnd[0])).to_bytes(4, 'big')
    buf += IPEnd[1].to_bytes(2, 'little')
    return buf


if __name__ == "__main__":
    port = (512).to_bytes(2, 'big')
    print(port)
    print(port[0])
    print(port[1])
    print("FIN")