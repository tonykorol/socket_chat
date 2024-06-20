import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 8008

SRV_ADDR = (HOST, PORT)

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv_sock.bind(SRV_ADDR)
srv_sock.listen()

clients = []
usernames = {}


def send_msg(message):
    for client in clients:
        try:
            client.send(message)
        except BrokenPipeError:
            close_conn(client)


def close_conn(client):
    client.close()
    clients.remove(client)
    send_msg(f"Client {usernames[client]} disconnected".encode("utf-8"))
    print(f"Client {usernames[client]} disconnected")
    del usernames[client]


def receive(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
        except:
            break
        message = f"{usernames[client]}: {message}".encode("utf-8")
        send_msg(message)


def connect():
    while True:
        client, addr = srv_sock.accept()

        client.send("Username: ".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        print(f"Connect to {addr} with username {username}")

        clients.append(client)
        usernames[client] = username

        client.send(f"Successful connect to server with username {username}\n".encode("utf-8"))
        send_msg(f"Client {username} joined the chat".encode("utf-8"))

        thread = Thread(target=receive, args=(client, ))
        thread.start()
        # receive(client)

print("Start server...")
connect()
