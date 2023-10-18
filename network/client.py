# TCP Client Socket
import socket

# TODO: add as .env variables
HOST = "localhost"
PORT = 9999

def login(username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to the server
        client.connect((HOST, PORT))
        # send the username and password separated by a newline
        client.send((username + "\n" + password).encode())
        # receive the response
        response = client.recv(1024).decode()
        # print out the response (testing)
        print("From client.py:", response)
        return response
    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"
    finally:
        client.close()

def register(username, password):
    # TODO: implement register
    print("Registered")
