import socket

def find_host():
	h = socket.gethostname()
	h = socket.gethostbyname(h)
	return h
