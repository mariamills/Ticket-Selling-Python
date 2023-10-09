import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 9999))
server.listen()

def establishConnection(client):
    client.send("Username:".encode())
    username = client.recv(1024).decode()

    client.send("Password:".encode())
    password = client.recv(1024).decode()

    #database connection(JSON or SQLITE) will be added here
while 1:
    client, IPaddress = server.accept()
    threading.Thread(target = establishConnection, args = (client,)).start()