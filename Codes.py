from enum import IntEnum, IntFlag


class QOSb(IntEnum):
    eve = 0

class QOSf(IntFlag):
    eve = 1 << QOSb.eve
    

class ShitnetCodes(IntEnum):
    listHosts = 3
    register = 4
    unregister = 5
    connectToHost = 6
    clearHosts = 7

class ClientCodes(IntEnum):
    hostList = 4