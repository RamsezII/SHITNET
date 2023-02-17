from enum import IntEnum, IntFlag


class Codes(IntEnum):
	start = 0
	kill = 1
	addEve = 2
	removeEve = 3
	listHosts = 4
	joinHost = 5
	clearHosts = 6
	hostPassword = 7
	holepunchTimeoutTest = 8
	publicIP = 10
	holePunch = 11
	yes = 12
	no = 13
	missingHost = 14
	wrongPass = 15
        

class QOSb(IntEnum):
	eve = 0
	ack = 1
	reliable = 2
	ordered = 3
	fragmented = 4

class QOSf(IntFlag):
	eve = 1 << 0
	ack = 1 << 1
	reliable = 1 << 2
	ordered = 1 << 3
	fragmented = 1 << 4

class QOSi(IntEnum):
	qos = 0
	paquetId = 1
	attempt = 2
	last = 3
