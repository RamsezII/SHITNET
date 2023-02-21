from enum import IntEnum, IntFlag


class Codes(IntEnum):
	addEve = 1
	getPublicEnd = 2
	firewallTest = 3
	listHosts = 4
	joinByName = 5
	joinByIP = 6
	prvPass = 7
	pubPass = 8
	rmEve = 9
	rsEve = 10
	holePunch = 13
	missingHost = 14
	alreadyHost = 15
	no = 16
	wrongPass = 17
	yes = 18
        

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
