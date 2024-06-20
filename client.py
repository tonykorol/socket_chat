import socket
from threading import Thread

SRV_ADDR = ("127.0.0.1", 8008)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SRV_ADDR)


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "Username: ":
                print(message, end='')
                username = input()
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            client.close()
            break


def send_msg():
    while True:
        message = input()
        if message == "exit":
            client.close()
            break
        client.send(message.encode("utf-8"))


receive_thread = Thread(target=receive)
receive_thread.start()

send_thread = Thread(target=send_msg)
send_thread.start()
