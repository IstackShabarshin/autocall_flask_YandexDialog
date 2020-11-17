import os, socket
import parser
import json

SOCKET_FILE = './tmp/natasha.socket'
SOCKET_TIMEOUT = 3.0

def SplitOnSegments(string):
    resp = conn_natasha(string, '-s')
    resp = json.loads(resp.replace("\'", '\"'))
    if type(resp) == type([]):
        return resp
    else:
        raise TypeError(resp)

def Normalize(req):
    resp = conn_natasha(req, '-n')
    resp = json.loads(resp.replace("\'", '\"'))
    if type(resp) == type([]):
        return resp
    else:
        raise TypeError(resp)

def FindNames(req):
    resp = conn_natasha(req, '-fn')
    resp = json.loads(resp.replace("\'", '\"'))
    if type(resp) == type([{}]):
        return resp
    else:
        raise TypeError(resp)

def FindDates(req):
    resp = conn_natasha(req, '-fd')
    resp = json.loads(resp.replace("\'", '\"'))
    if type(resp) == type([{}]):
        return resp
    else:
        raise TypeError(resp)

def FindAddrs(req):
    resp = conn_natasha(req, '-fa')
    resp = json.loads(resp.replace("\'", '\"'))
    if type(resp) == type([{}]):
        return resp
    else:
        raise TypeError(resp)

def conn_natasha(req, param):
    if os.path.exists(SOCKET_FILE):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        client.connect(SOCKET_FILE)
        try:
            client.send(str([req, param]).encode())

            resp = client.recv(1024).decode()
            return resp
        finally:
            client.close()
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
                conn.settimeout(SOCKET_TIMEOUT)
                message = conn.recv(1024).decode()
                message = json.loads(message.replace("\'", '\"'))
                string = message[0]
                param = message[1]
                if not string:
                    raise ValueError("string - " + string)
                if not param:
                    raise ValueError("param - " + param)

                #param parsing
                log_string = ''
                if param == '-n': #Normalize
                    log_string = 'Normalize func out = '
                    request = parser.Normalize(string)
                elif param == '-s': #Segments
                    log_string = 'SplitOnSegments func out = '
                    request = parser.SplitOnSegments(string)
                elif param == '-fn': #FindNames
                    log_string = 'FindNames func out = '
                    request = parser.FindNames(string)
                elif param == '-fd': #FindDates
                    log_string = 'FindDates func out = '
                    request = parser.FindDates(string)
                elif param == '-fa': #FindAddrs
                    log_string = 'FindAddrs func out = '
                    request = parser.FindAddrs(string)
                else:
                    raise ValueError(param)

                print('    Sending: '+ log_string + str(request), flush=True)
                conn.send(str(request).encode())
            except socket.timeout:
                print('    Socket timeout', flush=True)
            finally:
                conn.close()
    finally:
        print("Closing server...");
        server.close()
        os.remove(SOCKET_FILE)
        print("Closed")
