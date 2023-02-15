from enum import IntEnum, IntFlag


class Codes(IntEnum):
	start = 0
	kill = 1
	hostName = 2
	addEve = 3
	removeEve = 4
	listHosts = 5
	joinHost = 6
	clearHosts = 7
	hostPassword = 8
	keepAlive = 10
	yes = 11
	no = 12
	missingHost = 13
	wrongPass = 14
        
		
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
	last = 3
