import socket

from Buffer import *
from Codes import *
from Hosts import *
from SysArgs import *


class EVE():
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        print("server listening on:", self.sock.getsockname())
        self.hosts = Hosts()


    def update(self):
        message, self.recEnd = self.sock.recvfrom(1500)
        if len(message) == 0:
            print("empty from:", self.recEnd)
        else:
            # print("sender:", sender, "| message:", pullStringArray(message).decode(utfCode))
            reader = BufferReader(message)
            recQos = QOSf(reader.readByte())
            id = reader.readByte()
            attempt = reader.readByte()

            writer = bytearray(3)
            writer[QOSi.qos] = QOSf.ack
            writer[QOSi.paquetId] = id
            writer[QOSi.attempt] = attempt

            if len(message) == QOSi.last:
                if self.recEnd in self.hosts:
                    self.hosts[self.recEnd].time = time.time()
                    writer.append(Codes.yes)
                else:
                    writer.append(Codes.missingHost)
            else:
                while reader.hasNext():
                    recCode = Codes(reader.readByte())
                    if recCode == Codes.firewallTest:
                        self.holePunchTimeoutTest(self.recEnd)
                    elif recCode == Codes.getPublicEnd:
                        writer += ipendToBytes(self.recEnd)
                    elif recCode == Codes.addEve:
                        self.hosts.addHost(self.recEnd, reader, writer)
                    elif recCode == Codes.rmEve:
                        self.hosts.popHost(self.recEnd)
                    elif recCode == Codes.listHosts:
                        writer[QOSi.qos] |= QOSf.fragmented
                        self.hosts.writeToBuffer(writer)
                    elif recCode == Codes.joinByName:
                        self.joinHost(writer, reader)
                    elif recCode == Codes.yes:
                        pass
                    elif recCode == Codes.rsEve:
                        self.hosts.clear()
            self.sock.sendto(writer, self.recEnd)
    

    def joinHost(self, recWriter:bytearray, recReader:BufferReader):
        incomingLocalEnd = recReader.readBytes(6)
        nameBytes = recReader.pullString_cs()
        publicPassBytes = recReader.pullString_cs()
        self.hosts.necroCheck()
        for hostEnd in self.hosts:
            host:Host = self.hosts[hostEnd]
            if host.nameBytes == nameBytes:
                if host.passBytes == publicPassBytes:
                    recWriter.append(Codes.yes)
                    recWriter.append(Codes.holePunch)
                    recWriter += host.localEndBytes
                    recWriter += ipendToBytes(hostEnd)
                    # warn host to mirror holepunch
                    writer = bytearray(QOSi.last)
                    writer[QOSi.qos] = QOSf.eve
                    writer.append(Codes.holePunch)
                    writer += incomingLocalEnd
                    writer += ipendToBytes(self.recEnd)
                    self.sock.sendto(writer, hostEnd)
                else:
                    recWriter.append(Codes.wrongPass)
                return
        recWriter.append(Codes.missingHost)
    

    def holePunchTimeoutTest(self, sender):
        i = 0
        while True:
            time.sleep(1)
            i += 1
            writer = bytearray(3)
            writer[QOSi.qos] = QOSf.ack | QOSf.eve
            writer.append(Codes.firewallTest)
            writer.append(i)
            self.sock.sendto(writer, sender)


if __name__ == "__main__":    
    _port = "-p"
    args = sysArgs(_port)
    if _port in args:
        port = int(args[_port])
    else:
        port = 65000
    main = EVE(port)
    while True:
        main.update()