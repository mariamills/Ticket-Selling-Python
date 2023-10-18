# TCP Server Socket
import socket
import threading

# TODO: add as .env variables
HOST = "localhost"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
print("Server is ready to recieve")

def establishConnection(client):
    print("Connection established with client")
    try:
        # receive the data (username and password) from the client
        data = client.recv(1024).decode()

        # split the data into username and password (separated by a newline)
        # im doing this because it kept receiving the data as one string (e.g: username: 'adminadmin' instead of 'admin' and 'admin')
        username, password = data.split("\n", 1)
        # print the username and password (testing)
        print("Received username:", username)
        print("Received password:", password)

        # TODO: database connection(JSON or SQLITE) will be added here

        # check the username and password (testing)
        if username == "admin" and password == "admin":
            # send the response and say that the login was successful
            client.send("Login successful".encode())
        else:
            # send the response and say that the login failed
            client.send("Login failed".encode())
    # if there is a connection error, print it
    except socket.error as err:
        print(f"Connection error: {err}")

while 1:
    # accept the connection from the client
    client, IPaddress = server.accept()
    print(f"Accepted connection from {IPaddress}")

    # create a thread for each client
    thread = threading.Thread(target=establishConnection, args=(client,))
    # make the thread a daemon thread, so it closes when the main thread(program) closes
    thread.daemon = True
    # start the thread
    thread.start()
    print(f"Thread started for client {IPaddress}")

