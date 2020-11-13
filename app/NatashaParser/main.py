import os, socket
import NatashaParser

SOCKET_FILE = './tmp/natasha.socket'

if os.path.exists(SOCKET_FILE):
    os.remove(SOCKET_FILE)

print("Open UNIX socket")
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_FILE)
server.listen(1)

print("Licenning...")
#conn, _ = server.accept()
while True:
    conn, _ = server.accept()
    datagram = conn.recv(1024).decode()
    if not datagram:
        break
    else:
        print("-" * 20, flush=True)
    print(datagram, flush=True)
    request = NatashaParser.Normalize(datagram)
    print(request)
    for elem in request:
        conn.send(elem.encode())
    conn.close()

print("Closing...");
server.close()
os.remove(SOCKET_FILE)
print("Closed")
