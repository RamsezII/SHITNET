from enum import IntEnum, IntFlag


class Codes(IntEnum):
	addEve = 1
	getPublicEnd = 2
	firewallTest = 3
	holePunch = 4
	listHosts = 5
	joinByName = 6
	ping = 8
	removeEve = 9
	resetEve = 10
	alreadyHost = 12
	missingHost = 15
	no = 16
	wrongPass = 17
	yes = 18


class QOSf(IntFlag):
	Eve = 1 << 0
	Ack = 1 << 1
	Reliable = 1 << 2
	Ordered = 1 << 3
	Fragmented = 1 << 4
	Broadcast = 1 << 5

class QOSi(IntEnum):
	version = 0
	qos = 1
	id = 2
	attempt = 3
	netid = 4
	last = 5
