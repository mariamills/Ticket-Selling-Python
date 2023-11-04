# TCP Client Socket
import socket
import os
from dotenv import load_dotenv
from threading import Lock

# load the .env file
load_dotenv()

# environment variables
HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))

# commands to send to the server
COMMANDS = {
    "login": "login",
    "register": "register",
    "admin_check": "admin_check",
    "get_tickets": "get_tickets",
    "get_user_tickets": "get_user_tickets",
    "buy_ticket": "buy_ticket",
    "sell_ticket": "sell_ticket",
    "get_currency": "get_currency",
    "logout": "logout"
}

# create a PERSISTENT client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# set a timeout for the socket
client_socket.settimeout(10.0)  # Set a 10-second timeout for example

# lock for sending commands to the server (to prevent overlapping messages)
send_lock = Lock()


def send_command(command, message=""):
    """Sends a command to the server"""
    with send_lock:
        try:
            print("Sending command:", command)
            full_message = f"{command}\n{message}"
            client_socket.send(full_message.encode())
            print("Message sent")
        except socket.error as e:
            print(f"Send failed: {e}")
            return "Send failed"

def receive_response():
    """Receives a response from the server"""
    try:
        response = client_socket.recv(1024).decode()
        print("Response received:", response)
        return response
    except socket.error as e:
        return "Receive failed"



def login(username, password):
    send_command("login", f"{username}\n{password}")
    response = receive_response()
    print("From client.py - Login:", response)
    return response


def register(first_name, last_name, email, username, password):
    print("From client.py - Register:", first_name, last_name, email, username, password)
    send_command("register", f"{first_name}\n{last_name}\n{email}\n{username}\n{password}")
    response = receive_response()
    print("From client.py - Register:", response)
    return response


def get_currency(username):
    send_command("get_currency", username)
    response = receive_response()
    return response


def get_tickets():
    send_command("get_tickets")
    return receive_response()


def get_user_tickets(username):
    send_command("get_user_tickets", username)
    return receive_response()


def admin_check(username):
    send_command("admin_check", username)
    return receive_response()


def buy_ticket(ticket_id, username):
    send_command("buy_ticket", f"{ticket_id}\n{username}")
    return receive_response()


def sell_ticket(ticket_id, username):
    send_command("sell_ticket", f"{ticket_id}\n{username}")
    return receive_response()


def logout():
    send_command("logout")
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    # close application
    exit()

# Admin Functions
def add_ticket(ticket_name, ticket_price, ticket_amount, ticket_date):
    send_command("add_ticket", f"{ticket_name}\n{ticket_price}\n{ticket_amount}\n{ticket_date}")
    return receive_response()

