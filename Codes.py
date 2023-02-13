from enum import IntEnum, IntFlag


class NetCodes(IntEnum):
	start = 0
	kill = 1
	register = 2
	unregister = 3
	listHosts = 4
	connectToHost = 5
	clearHosts = 6
        

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
