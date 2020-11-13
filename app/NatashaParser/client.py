import os
import socket

SOCKET_FILE = './tmp/natasha.socket'

def conn_natasha(string, param)
    print("Connecting...")
    if os.path.exists(SOCKET_FILE):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        client.connect(SOCKET_FILE)
        try:
            client.send(string.encode())
            client.send(param.encode())

            result = []
            resp = client.recv(1024).decode()
            result.append(resp)
            while (len(resp) > 0):
                resp = client.recv(1024).decode()
                result.append(resp)
        finally:
            client.close()
            return result
    else:
        raise FileNotFoundError(SOCKET_FILE)