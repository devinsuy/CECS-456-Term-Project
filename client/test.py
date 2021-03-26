from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

host = "localhost"
port = 5500
address = (host, port)
bufSize = 1024

messages = []
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)


def recieve_messages():
    """
    Receive messages from server
    :return: None
    """
    while True:
        try:
            msg = client_socket.recv(bufSize).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("Exception", e)
            break


def send_message(msg):
    """
    Send messages to server
    :param msg: str
    :return: None
    """
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


receive_thread = Thread(target=recieve_messages)
receive_thread.start()


send_message("Moua")
