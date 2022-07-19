import socket


def parseUrlForIP(host):
    host = host
    host = host.split("//")[1].split("/")[0]

    address = socket.gethostbyname_ex(host)
    ip = address[2]
    ip = ip[0]
    print(ip)