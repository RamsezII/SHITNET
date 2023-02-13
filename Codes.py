from enum import IntEnum, IntFlag


class ServerCodes(IntEnum):
	listHosts = 3
	register = 4
	unregister = 5
	connectToHost = 6
	clearHosts = 7


class ClientCodes(IntEnum):
    hostList = 4
    
    
class QOSb(IntEnum):
	ack = 0
	reliable = 1
	ordered = 2
	fragmented = 3

class QOSf(IntFlag):
	ack = 1 << 0
	reliable = 1 << 1
	ordered = 1 << 2
	fragmented = 1 << 3

class QOSi(IntEnum):
	qos = 0
	paquetId = 1
	attempt = 2
