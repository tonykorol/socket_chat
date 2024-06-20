import socket
import select

SRV_ADDR = ("127.0.0.1", 8008)

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv_sock.bind(SRV_ADDR)
srv_sock.setblocking(False)
srv_sock.listen(10)

STORE = {}

print("Start server")
FOR_READ = [srv_sock]
FOR_WRITE = []
FOR_ERR = []

for_resp = []

while True:
    r, w, e = select.select(FOR_READ, FOR_WRITE, FOR_ERR)

    for sock in r:
        if sock is srv_sock:
            client, addr = srv_sock.accept()
            STORE[client.fileno()] = {'addr': addr, "req": None}
            FOR_READ.append(client)
        else:
            try:
                data = sock.recv(2048)
            except OSError:
                del STORE[sock.fileno()]
                sock.close()
                # FOR_READ.remove(sock)
                continue
            STORE[sock.fileno()]["req"] = data.decode("utf-8")
            FOR_WRITE.append(sock)
            # FOR_READ.remove(sock)

    for sock in w:
        response = f"client {STORE[sock.fileno()]['addr']}, send: {STORE[sock.fileno()]['req']}"
        try:
            sock.send(response.encode('utf-8'))
        except OSError:
            del STORE[sock.fileno()]
            sock.close()
            # FOR_WRITE.remove(sock)
            continue
        STORE[sock.fileno()]['req'] = None
        # FOR_READ.append(sock)
        # FOR_WRITE.remove(sock)

    for sock in e:
        del STORE[sock.fileno()]
        sock.close()
        try:
            FOR_WRITE.remove(sock)
        except Exception:
            ...
        try:
            FOR_READ.remove(sock)
        except Exception:
            ...
        try:
            FOR_ERR.remove(sock)
        except Exception:
            ...


