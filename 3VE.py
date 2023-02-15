import ipaddress
import socket

from Buffer import *
from Codes import *
from Hosts import *
from SysArgs import *

#https://stackoverflow.com/questions/62903377/python3-bytes-vs-bytearray-and-converting-to-and-from-strings


class Main():

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        print("server listening on:", self.sock.getsockname())
        self.hosts = Hosts()


    def update(self):
        message, self.rec_end = self.sock.recvfrom(1500)
        if len(message) == 0:
            print("empty from:", self.rec_end)
        else:
            # print("sender:", sender, "| message:", pullStringArray(message).decode(utfCode))
            self.recReader = BufferReader(message)
            qos = QOSf(self.recReader.readByte())
            id = self.recReader.readByte()
            attempt = self.recReader.readByte()

            self.recWriter = bytearray(3)
            self.recWriter[QOSi.qos] = QOSf.ack
            self.recWriter[QOSi.paquetId] = id
            self.recWriter[QOSi.attempt] = attempt

            rec_code = Codes(self.recReader.readByte())
            # print("code:", rec_code)

            if rec_code == Codes.addEve:
                self.hosts.addHost(self.rec_end, self.recReader.pullStringBytes(), self.recReader.pullStringBytes())
            elif rec_code == Codes.keepAlive:
                if self.rec_end in self.hosts:
                    self.hosts[self.rec_end].time = time.time()
                    self.recWriter.append(Codes.yes)
                else:
                    self.recWriter.append(Codes.missingHost)
            elif rec_code == Codes.removeEve:
                self.hosts.popHost(self.rec_end)
            elif rec_code == Codes.listHosts:
                self.sendHostList()
            elif rec_code == Codes.joinHost:
                self.joinHost(self.recReader.pullStringBytes(), self.recReader.pullStringBytes())
            elif rec_code == Codes.clearHosts:
                self.hosts.clear()

            self.sock.sendto(self.recWriter, self.rec_end)


    def sendHostList(self):
        self.recWriter[QOSi.qos] |= QOSf.fragmented
        self.hosts.writeToBuffer(self.recWriter)
    

    def joinHost(self, nameBytes, publicPassBytes):
        for hostEnd in self.hosts:
            host = self.hosts[hostEnd]
            if host.nameBytes == nameBytes:
                if host.passBytes != publicPassBytes:
                    self.recWriter.append(Codes.wrongPass)
                else:
                    self.recWriter.append(Codes.yes)
                    self.recWriter += writeIPEndToBuf(hostEnd)
                    
                    writer = bytearray(QOSi.last)
                    writer[QOSi.qos] = QOSf.nocheck
                    writer.append(Codes.joinHost)
                    writer += writeIPEndToBuf(self.rec_end)
                    self.sock.sendto(writer, hostEnd)
                return
        self.recWriter.append(Codes.missingHost)


if __name__ == "__main__":    
    _port = "-port"
    args = sysArgs(_port)
    if _port in args:
        port = int(args[_port])
    else:
        port = 65000
    main = Main(port)
    while True:
        main.update()