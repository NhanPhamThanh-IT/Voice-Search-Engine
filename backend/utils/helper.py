import socket

def get_ipv4_address():
    hostname = socket.gethostname()
    ipv4_address = socket.gethostbyname(hostname)
    return ipv4_address
