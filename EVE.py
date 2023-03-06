import socket

from Buffer import *
from Codes import *
from Hosts import *
from SysArgs import *


class EVE():
    version = 0

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        print("server listening on", self.sock.getsockname()[1])
        self.hosts = Hosts()


    def update(self):
        message, self.recEnd = self.sock.recvfrom(1500)
        if len(message) == 0:
            print("empty from:", self.recEnd)
        else:
            reader = BufferReader(message)
            msgID = reader.buffer[QOSi.id]
            attempt = reader.buffer[QOSi.attempt]
            reader.iread = QOSi.last

            writer = bytearray(QOSi.last)
            writer[QOSi.qos] = QOSf.Ack
            writer[QOSi.id] = msgID
            writer[QOSi.attempt] = attempt

            if len(message) == QOSi.last:
                if self.recEnd in self.hosts:
                    self.hosts[self.recEnd].time = time.time()
            else:
                while reader.hasNext():
                    recCode = Codes(reader.readByte())
                    if recCode == Codes.firewallTest:
                        self.holePunchTimeoutTest(self.recEnd)
                    elif recCode == Codes.holePunch:
                        self.holePunch(writer, reader)
                    elif recCode == Codes.getPublicEnd:
                        writer += netendToBytes(self.recEnd)
                    elif recCode == Codes.addEve:
                        self.hosts.addHost(self.recEnd, reader, writer)
                    elif recCode == Codes.removeEve:
                        self.hosts.popHost(self.recEnd)
                    elif recCode == Codes.listHosts:
                        self.hosts.writeToBuffer(writer)
                    elif recCode == Codes.joinByName:
                        self.joinHost(writer, reader)
                    elif recCode == Codes.yes:
                        pass
                    elif recCode == Codes.resetEve:
                        self.hosts.clear()
            self.sock.sendto(writer, self.recEnd)
    

    def holePunch(self, recWriter:bytearray, recReader:BufferReader):
        incomingLocalEnd = recReader.readBytes(6)
        nameBytes = recReader.pullString_cs()
        self.hosts.necroCheck()
        for hostEnd in self.hosts:
            host:Host = self.hosts[hostEnd]
            if host.nameBytes == nameBytes:
                recWriter.append(Codes.yes)
                recWriter += host.localEndBytes
                recWriter += netendToBytes(hostEnd)
                # warn host to mirror holepunch
                writer = bytearray(QOSi.last)
                writer[QOSi.qos] = QOSf.Eve
                writer.append(Codes.holePunch)
                writer += incomingLocalEnd
                writer += netendToBytes(self.recEnd)
                self.sock.sendto(writer, hostEnd)
                return
        recWriter.append(Codes.missingHost)
    

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
                    recWriter += host.localEndBytes
                    recWriter += netendToBytes(hostEnd)
                    # warn host to mirror holepunch
                    writer = bytearray(QOSi.last)
                    writer[QOSi.qos] = QOSf.Eve
                    writer.append(Codes.holePunch)
                    writer += incomingLocalEnd
                    writer += netendToBytes(self.recEnd)
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
            writer = bytearray(QOSi.last)
            writer[QOSi.qos] = QOSf.Ack | QOSf.Eve
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