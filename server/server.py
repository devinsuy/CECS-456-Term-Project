from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global Constants
host = 'localhost'
port = 5500
bufSize = 1024
address = (host, port)
max_con = 10

# Global Variables
persons = []
server = socket(AF_INET, SOCK_STREAM)
server.bind(address)    # set up server


def broadcast(msg, name):
    """
    Send new message to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return: None
    """
    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf8") + msg)

def client_connection(person):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = person.client

    # get persons name
    name = client.recv(bufSize).decode("utf8")
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, name)  # broadcast welcome message

    while True:
        try:
            msg = client.recv(bufSize)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"):
                broadcast(f"{name} has left the chat...", "")
                client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
                break
            else:
                broadcast(msg, name)
        except Exception as e:
            print("Exception", e)
            break


def connecting():
    """
    Wait for connection from new clients, start new thread once connected
    :param server: socket
    :return:None
    """
    run = True
    while run:
        try:
            client, addr = server.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"Connection: {addr} connected to the server at {time.time()}")
            Thread(target=client_connection, args=(person,)).start()
        except Exception as e:
            print("FAILED", e)
            run = False
    print("Server Crashed!")


if __name__ == "__main__":
    server.listen(max_con)    # listen up to x connections
    print("Connected, Waiting for connection...")
    accept_thread = Thread(target=connecting)
    accept_thread.start()
    accept_thread.join()
    server.close()
