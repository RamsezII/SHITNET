from enum import IntEnum, IntFlag


class NetCodes(IntEnum):
	start = 0
	kill = 1
	hostName = 2
	register = 3
	unregister = 4
	listHosts = 5
	joinHost = 6
	clearHosts = 7
	hostPassword = 8
	keepAlive = 9
        

class QOSb(IntEnum):
	nocheck = 0
	ack = 1
	reliable = 2
	ordered = 3
	fragmented = 4

class QOSf(IntFlag):
	nocheck = 1 << 0
	ack = 1 << 1
	reliable = 1 << 2
	ordered = 1 << 3
	fragmented = 1 << 4

class QOSi(IntEnum):
	qos = 0
	paquetId = 1
	attempt = 2

