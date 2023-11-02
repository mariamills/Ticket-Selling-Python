# TCP Client Socket
import socket
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()

# environment variables
HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))

# commands
LOGIN_COMMAND = "login"
REGISTER_COMMAND = "register"
ADMIN_CHECK_COMMAND = "admin_check"
GET_TICKETS_COMMAND = "get_tickets"
GET_USER_TICKETS_COMMAND = "get_user_tickets"
BUY_TICKET_COMMAND = "buy_ticket"
SELL_TICKET_COMMAND = "sell_ticket"
GET_CURRENCY_COMMAND = "get_currency"
LOGOUT_COMMAND = "logout"


def send_command(client, command, message=""):
    message = f"{command}\n{message}"
    client.send(message.encode())


# login function - returns a response from the server
def login(username, password):
    # create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to the server
        client.connect((HOST, PORT))

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


# check if the user is an admin
def admin_check(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))

        message = f"{username}"

        send_command(client, ADMIN_CHECK_COMMAND, message)

        response = client.recv(1024).decode()
        if response.startswith("admin:"):
            admin_status = response.split(":")[1]
            print("Admin status:", admin_status)
        else:
            print(response)

        return response

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"
    finally:
        client.close()


# update for viewing tickets
def get_tickets():
    # create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to the server
        client.connect((HOST, PORT))

        # send the login command
        send_command(client, GET_TICKETS_COMMAND)

        # receive the response from the server
        response = client.recv(1024).decode()

        # print out the response (testing)
        print("From client.py - View Tickets:", response)
        return response

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"

    finally:
        client.close()


# get tickets for a specific user
def get_user_tickets(username):
    # create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to the server
        client.connect((HOST, PORT))

        # send the login command
        send_command(client, GET_USER_TICKETS_COMMAND, username)

        # receive the response from the server
        response = client.recv(1024).decode()

        # print out the response (testing)
        print("From client.py - View Tickets:", response)

        # Split the response into a list of tickets, and then split each ticket's details
        ticket_list = [ticket.split(', ') for ticket in response.split('\n') if ticket]
        return ticket_list

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"

    finally:
        client.close()


def buy_ticket(event_id, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))

        message = f"{event_id}\n{username}"

        send_command(client, BUY_TICKET_COMMAND, message)

        response = client.recv(1024).decode()
        print("From client.py - Buy Ticket:", response)

        # If insufficient funds
        if response == "Insufficient funds":
            # TODO: Popup window to notify user
            print("Insufficient funds - client")
        else:
            print("Ticket purchased successfully - client")

        return response

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"
    finally:
        client.close()


# sell ticket
def sell_ticket(event_name, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))

        message = f"{event_name}\n{username}"

        send_command(client, SELL_TICKET_COMMAND, message)

        response = client.recv(1024).decode()
        print("From client.py - Sell Ticket:", response)
        return response

    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"
    finally:
        client.close()


def get_currency(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        send_command(client, GET_CURRENCY_COMMAND, username)
        response = client.recv(1024).decode()
        print("From client.py - Get Currency:", response)
        return response
    except socket.error as err:
        print(f"Connection error: {err}")
        return f"Connection error: {err}"
    finally:
        client.close()


# logout - closes the client socket connection to the server
def logout():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        send_command(client, LOGOUT_COMMAND, "")
        print("Sent logout command to server")
    except socket.error as err:
        print(f"Connection error: {err}")
    finally:
        client.close()


