
import os
import socket

SOCKET_FILE = './echo.socket'

print("Connecting...")
if os.path.exists(SOCKET_FILE):
    client1 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    client1.connect(SOCKET_FILE)
    print("Connected")
    print("Ctrl-C to close")
    print("Send 'DONE' to stop server")
    try:
        x = input("> ")
        if "" != x:
            print("SENDED: %s" % x)
            client1.send(x.encode())

            result = []
            resp = client1.recv(1024).decode()
            result.append(resp)
            while (len(resp) > 0):
                resp = client1.recv(1024).decode()
                result.append(resp)

            print(result)

    except KeyboardInterrupt as k:
        print("STOPPING client")
    finally:
        client1.close()
else:
    print("Can't connect to server")
print("Executed")
