import os, socket
from parser import (
    FindNames,
    FindDates,
    FindAddrs,
    Normalize
)

SOCKET_FILE = './tmp/natasha.socket'

def conn_natasha(string, param):
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

def main():
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

    print("Open UNIX socket", flush=True)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_FILE)
    server.listen(1)

    print("Licenning...")
    try:
        while True:
            try:
                print("Open new connect")
                conn, _ = server.accept()
                string = conn.recv(1024).decode()
                param = conn.recv(1024).decode()
                if not string or not param:
                    break
                else:
                    raise ValueError(string)

                #param parsing
                if param == '-n': #Normalize
                    request = Normalize(string)
                elif param == '-fn': #FindNames
                    request = FindNames(string)
                elif param == '-fd': #FindDates
                    request = FindDates(string)
                elif param == '-fa': #FindAddrs
                    request = FindAddrs(string)
                else:
                    raise ValueError(param)

                for elem in request:
                    conn.send(elem.encode())
            finally:
                print("Close connect")
                conn.close()
    finally:
        print("Closing server...");
        server.close()
        os.remove(SOCKET_FILE)
        print("Closed")

if __name__ == "__main__":
    main()
