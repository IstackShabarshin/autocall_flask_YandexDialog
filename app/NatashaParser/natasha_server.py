import os, socket
import parser
#from parser import (
#    SplitOnSegments,
#    FindNames,
#    FindDates,
#    FindAddrs,
#    Normalize
#)

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

def start_listennig():
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

    print("Open UNIX socket", flush=True)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_FILE)
    server.listen(1)

    print("Lictenning...", flush=True)
    try:
        while True:
            try:
                conn, _ = server.accept()
                print("Open new connect", flush=True)
                string = conn.recv(1024).decode()
                param = conn.recv(1024).decode()
                #print(string + param, flush=True)
                if not string:
                    raise ValueError("string - " + string)
                if not param:
                    raise ValueError("param - " + string)

                #param parsing
                if param == '-n': #Normalize
                    request = parser.Normalize(string)
                elif param == '-s': #Segments
                    request = parser.SplitOnSegments(string)
                elif param == '-fn': #FindNames
                    request = parser.FindNames(string)
                elif param == '-fd': #FindDates
                    request = parser.FindDates(string)
                elif param == '-fa': #FindAddrs
                    request = parser.FindAddrs(string)
                else:
                    raise ValueError(param)

                for elem in request:
                    conn.send(elem.encode())
            finally:
                print("Close connect", flush=True)
                conn.close()
    finally:
        print("Closing server...");
        server.close()
        os.remove(SOCKET_FILE)
        print("Closed")
