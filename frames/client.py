# TCP Client Socket
import socket
import os
import hashlib
from dotenv import load_dotenv

# load the .env file
load_dotenv()

# environment variables
HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))

# commands
LOGIN_COMMAND = "login"
REGISTER_COMMAND = "register"
#***Update for tickets
VIEW_TICKETS_COMMAND = "view_tickets"

def send_command(client, command, message):
    message = f"{command}\n{message}"
    client.send(message.encode())

# login function - returns a response from the server
def login(username, password):
    # create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to the server
        client.connect((HOST, PORT))
        #password = hashlib.sha256(password.encode()).hexdigest()
        
        # create the message to send to the server
        message = f"{username}\n{password}"

        # send the login command
        send_command(client, LOGIN_COMMAND, message)

        # receive the response from the server
        response = client.recv(1024).decode()

        # print out the response (testing)
        print("From client.py - Login:", response)
        return response

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"

    finally:
        client.close()

def register(first_name, last_name, email, username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))

        message = f"{first_name}\n{last_name}\n{email}\n{username}\n{password}"

        send_command(client, REGISTER_COMMAND, message)

        response = client.recv(1024).decode()
        print("From client.py - Register:", response)
        return response

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"
    finally:
        client.close()




#****update for viewing tickets
def view_tickets():
    # create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to the server
        client.connect((HOST, PORT))

        # create the message to send to the server
        message = f"test"

        # send the login command
        send_command(client, VIEW_TICKETS_COMMAND, message)

        # receive the response from the server
        response = client.recv(1024).decode()
        response1= "client.recv(1024)"

        # print out the response (testing)
        print("From client.py - View Tickets:", response)
        return response
  

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"

    finally:
        client.close()

