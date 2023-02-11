from enum import IntEnum, IntFlag


class QOSb(IntEnum):
    eve = 0

class QOSf(IntFlag):
    eve = 1 << QOSb.eve
    

class ShitnetB(IntEnum):
    listHosts = 1
    register = 2
    unregister = 3
    connectToHost = 4
    clear = 5

class ClientB(IntEnum):
    hostList = 4