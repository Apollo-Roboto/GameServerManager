import psutil

def isPortUsed(port):
	for conn in psutil.net_connections():
		if(port == conn.laddr.port):
			return True
	return False