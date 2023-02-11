from enum import IntEnum


class ShitnetCodes(IntEnum):
    listHosts = 3
    register = 4
    unregister = 5
    connectToHost = 6
    clearHosts = 7

class ClientCodes(IntEnum):
    hostList = 4