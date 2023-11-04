# TCP Server Socket
import socket
import threading
import sqlite3
import os
from dotenv import load_dotenv
from datetime import date

# load the .env file
load_dotenv()

# get the host and port from the .env file
HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))

# path to the database - using the os module to get the path to the project directory, so it works on any machine
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'project.db')

# create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the host and port
server.bind((HOST, PORT))

# listen for connections
server.listen()
print("Server is ready to receive")


def establish_connection(client):
    """Establish a connection with the client"""
    try:
        # keep the socket connection open until the client sends "logout"
        while True:
            # receive the data (username and password) from the client
            message = client.recv(1024).decode()
            print("Received message:", message)

            # split the data into command and message (separated by a newline)
            command, data = message.split("\n", 1)

            # based on the command sent from client, call the appropriate function
            match command:
                case "login":
                    handle_login(data)
                case "register":
                    handle_register(data)
                case "get_user_tickets":
                    handle_get_user_tickets(data)
                case "get_tickets":
                    handle_get_tickets()
                case "buy_ticket":
                    handle_buy_ticket(data)
                case "sell_ticket":
                    handle_sell_ticket(data)
                case "admin_check":
                    handle_admin_check(data)
                case "get_currency":
                    handle_get_currency(data)
                case "logout":
                    handle_logout()
                    break
                case _:
                    print("Invalid command")
                    handle_logout()
                    break

    # if there is a connection error, print it
    except socket.error as err:
        print(f"Connection error: {err}")
    finally:
        client.close()  # Ensure the connection is closed when done


# handle login
def handle_login(data):
    # split the data into username and password (separated by a newline)
    username, password = data.split("\n", 1)

    # use context manager to connect to sqlite database
    with sqlite3.connect(DB_PATH) as conn:
        # create a cursor
        c = conn.cursor()

        # check if the username and password are correct
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        # fetch the user - if one exists with those credentials, it will be returned
        user = c.fetchone()

    # if the username and password are correct, send a success message to the client
    if user:
        # TODO: Remove these print statements - keeping for testing purposes now (still in use)
        print("Login successful on server - sending success message to client")
        client.send("Login successful".encode())
    else:
        print("Login failed on server - sending failure message to client")
        client.send("Login failed".encode())
        # close the connection with the client
        client.close()


# handle register
def handle_register(data):
    # split the message into first name, last name, email, username, password (separated by a newline)
    first_name, last_name, email, username, password = data.split("\n", 4)

    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    # create a cursor
    c = conn.cursor()

    # check if the username already exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    # if the username already exists, send a failure message to the client
    if user:
        print("Register failed on server - USERNAME ALREADY EXISTS - sending failure message to client")
        client.send("Username Exists".encode())
    else:
        # insert the user into the database
        c.execute("INSERT INTO users (first_name, last_name, email, username, password) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, email, username, password))
        conn.commit()
        print("Register successful on server - sending success message to client")
        client.send("Register successful".encode())


# get the tickets for the current user
def handle_get_user_tickets(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # get all user's transactions including event_id, total cost, and amount
        query = """SELECT concerts.event_name, transactions.total, transactions.amount 
                   FROM transactions 
                   JOIN concerts ON transactions.event_id = concerts.event_id
                   WHERE transactions.username = ?"""
        # execute the query, data is a tuple with one element, so we need to add a comma after the element
        c.execute(query, (username,))
        tickets = c.fetchall()

        if tickets:
            # Convert list of tuples to a formatted string
            tickets_str = "\n".join(f"{event_name}, {total_cost}, {amount}" for event_name, total_cost, amount in tickets)
            client.send(tickets_str.encode())
            # TODO: Remove this print statement - keeping for testing purposes now (still in use)
            print("Sent user tickets to client:", tickets_str)
        else:
            client.send("No tickets".encode())


# get all available concert tickets
def handle_get_tickets():
    print("Getting tickets")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # get the first 15 concerts
        c.execute("SELECT * FROM concerts LIMIT 15")
        tickets = c.fetchall()

        # convert the list of tuples to a string to send to the client
        # else the program freezes and crashes
        str_items = str(tickets)
        client.send(str_items.encode())


# buy a ticket
def handle_buy_ticket(data):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # split the data into event_id and username (separated by a newline)
        event_id, username = data.split("\n", 1)

        # get the price of the ticket
        c.execute("SELECT price FROM concerts WHERE event_id = ?", (event_id,))
        price = c.fetchone()[0]

        # get the user's funds
        c.execute("SELECT funds FROM users WHERE username = ?", (username,))
        funds = c.fetchone()[0]

        # check if the user has enough funds to buy the ticket
        if funds >= price:
            # subtract the price from the user's funds
            funds -= price

            # check if the user already has a ticket for this event
            c.execute("SELECT * FROM transactions WHERE username = ? AND event_id = ?", (username, event_id))
            existing_ticket = c.fetchone()

            if existing_ticket:
                # update the amount and total of the existing ticket
                new_amount = existing_ticket[3] + 1
                total = existing_ticket[4]
                c.execute("UPDATE transactions SET amount = ?, total = ? WHERE username = ? AND event_id = ?",
                          (new_amount, total, username, event_id))
            else:
                # add the ticket to the user's tickets
                c.execute("INSERT INTO transactions (username, event_id, amount, total, date) VALUES (?, ?, ?, ?, ?)",
                          (username, event_id, 1, price, date.today()))

            # update the user's funds
            c.execute("UPDATE users SET funds = ? WHERE username = ?", (funds, username))
            # subtract one from the amount of tickets available
            c.execute("UPDATE concerts SET amount = amount - 1 WHERE event_id = ?", (event_id,))

            conn.commit()
            client.send("Ticket purchased".encode())
        else:
            client.send("Insufficient funds".encode())


# sell a ticket
def handle_sell_ticket(data):
    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    # create a cursor
    c = conn.cursor()

    # split the data into event name and username (separated by a newline)
    event_name, username = data.split("\n", 1)

    # get the event_id of the ticket
    c.execute("SELECT event_id FROM concerts WHERE event_name = ?", (event_name,))
    event_id = c.fetchone()[0]

    # get the price of the ticket
    c.execute("SELECT price FROM concerts WHERE event_id = ?", (event_id,))
    price = c.fetchone()[0]

    # get the user's funds
    c.execute("SELECT funds FROM users WHERE username = ?", (username,))
    funds = c.fetchone()[0]

    # add the price to the user's funds
    funds += price
    # update the user's funds
    c.execute("UPDATE users SET funds = ? WHERE username = ?", (funds, username))

    # Check if the user has this ticket in their transactions
    c.execute("SELECT amount FROM transactions WHERE username = ? AND event_id = ?", (username, event_id))
    result = c.fetchone()
    if result:
        amount = result[0]
        if amount > 1:
            # If user has more than one ticket, decrease the amount
            c.execute("UPDATE transactions SET amount = amount - 1 WHERE username = ? AND event_id = ?",
                      (username, event_id))
        else:
            # If user has only one ticket, delete the transaction
            c.execute("DELETE FROM transactions WHERE username = ? AND event_id = ?", (username, event_id))

    # add one to the amount of tickets available
    c.execute("UPDATE concerts SET amount = amount + 1 WHERE event_id = ?", (event_id,))
    conn.commit()

    client.send("Ticket sold".encode())


# handle admin check - check if the user is an admin
def handle_admin_check(data):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # execute the query, data is a tuple with one element, so we need to add a comma after the element
        # sqlite expects a tuple (or list), even if there is only one element
        c.execute("SELECT admin FROM users WHERE username = ?", (data,))
        admin_status = c.fetchone()

        if admin_status[0] == 1:
            response = "ADMIN"
            client.send(response.encode())
        else:
            client.send("USER".encode())


def handle_get_currency(username):
    """Get the user's currency"""
    # connect to sqlite database
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT funds FROM users WHERE username = ?", (username,))
        funds = c.fetchone()[0]
        client.send(str(funds).encode())


def handle_logout():
    """Close the connection with the client"""
    print("Closing connection with client")
    client.shutdown(socket.SHUT_RDWR)
    client.close()


# Continuously listen for connections from clients - keep the server running
while True:
    try:
        # accept the connection from the client
        client, IPaddress = server.accept()
        print(f"Accepted connection from {IPaddress}")

        # create a thread for each client
        thread = threading.Thread(target=establish_connection, args=(client,))
        # make the thread a daemon thread, so it closes when the main thread(program) closes
        thread.daemon = True
        # start the thread
        thread.start()
        print(f"Thread started for client {IPaddress}")
    except socket.error as e:
        print(f"Error accepting connection: {e}")
