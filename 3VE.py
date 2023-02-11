import socket

from BufferReader import *
from Codes import *
from Hosts import *
from SysArgs import *
from Util import *


#https://stackoverflow.com/questions/62903377/python3-bytes-vs-bytearray-and-converting-to-and-from-strings

def loop(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    print("server listening on:", sock.getsockname())

    hosts = Hosts()

    while True:
        message, sender = sock.recvfrom(1500)
        if len(message) == 0:
            print("empty from:", sender)
        else:
            # print("sender:", sender, "| message:", pullStringArray(message).decode(utfCode))
            reader = BufferReader(message)
            code = ShitnetCodes(reader.readByte())
            print("code:", code)
            if code == ShitnetCodes.register:
                hostName = reader.pullStringBuffer(True)
                lifeTime = reader.readByte()
                hosts[sender] = Host(hostName, lifeTime)
                print("register:", sender, ", hostName:", hostName, ", lifeTime:", lifeTime)
            elif code == ShitnetCodes.listHosts:
                buf = bytearray(4)
                buf[0] = 0
                buf[1] = 0
                buf[2] = ClientCodes.hostList
                hosts.writeToBuffer(buf)
                sock.sendto(buf, sender)
                pass
            elif code == ShitnetCodes.connectToHost:
                pass
            elif code == ShitnetCodes.clearHosts:
                hosts.clear()


if __name__ == "__main__":    
    _port = "-port"
    args = sysArgs(_port)
    if _port in args:
        port = int(args[_port])
    else:
        port = 65000
    loop(port)