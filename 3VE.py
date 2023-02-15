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
        message, self.sender = self.sock.recvfrom(1500)
        if len(message) == 0:
            print("empty from:", self.sender)
        else:
            # print("sender:", sender, "| message:", pullStringArray(message).decode(utfCode))
            self.netReader = BufferReader(message)
            qos = QOSf(self.netReader.readByte())
            id = self.netReader.readByte()
            attempt = self.netReader.readByte()

            self.netWriter = bytearray(3)
            self.netWriter[QOSi.qos] = QOSf.ack
            self.netWriter[QOSi.paquetId] = id
            self.netWriter[QOSi.attempt] = attempt

            rec_code = NetCodes(self.netReader.readByte())
            # print("code:", rec_code)

            if rec_code == NetCodes.register:
                self.hosts.addHost(self.sender, self.netReader.pullStringBytes(True), self.netReader.pullStringBytes(True))
            elif rec_code == NetCodes.keepAlive:
                self.hosts[self.sender].time = time.time()
            elif rec_code == NetCodes.unregister:
                self.hosts.popHost(self.sender)
            elif rec_code == NetCodes.listHosts:
                self.sendHostList()
            elif rec_code == NetCodes.joinHost:
                self.joinHost(self.netReader.pullStringBytes(True), self.netReader.pullStringBytes(True))
            elif rec_code == NetCodes.clearHosts:
                self.hosts.clear()

            self.sock.sendto(self.netWriter, self.sender)


    def sendHostList(self):
        self.netWriter[QOSi.qos] |= QOSf.fragmented
        self.netWriter.append(NetCodes.listHosts)
        self.hosts.writeToBuffer(self.netWriter)
    

    def joinHost(self, nameBytes, passBytes):
        for host in self.hosts:
            if host.nameBytes == nameBytes:
                if host.passBytes == passBytes:
                    writer = bytearray(QOSi.last)
                    writer[QOSi.qos] = QOSf.ack | QOSf.nocheck
                    writer.append(NetCodes.joinHost)
                    self.sock.sendto(writer, self.sender)
                break


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