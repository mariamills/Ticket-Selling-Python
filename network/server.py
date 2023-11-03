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
        # receive the data (username and password) from the client
        message = client.recv(1024).decode()

        # split the data into command and message (separated by a newline)
        command, data = message.split("\n", 1)

        # based on the command sent from client, call the appropriate function
        match command:
            case "login":
                handle_login(client, data)
            case "register":
                handle_register(client, data)
            case "get_user_tickets":
                handle_get_user_tickets(client, data)
            case "get_tickets":
                handle_get_tickets(client)
            case "buy_ticket":
                handle_buy_ticket(client, data)
            case "sell_ticket":
                handle_sell_ticket(client, data)
            case "admin_check":
                handle_admin_check(client, data)
            case "get_currency":
                handle_get_currency(client, data)
            case "logout":
                handle_logout(client)
                return  # return to close the thread
            case _:
                print("Invalid command")
                handle_logout(client)

    # if there is a connection error, print it
    except socket.error as err:
        print(f"Connection error: {err}")


# handle login
def handle_login(client, data):
    # split the data into username and password (separated by a newline)
    username, password = data.split("\n", 1)

    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    # create a cursor
    c = conn.cursor()

    # check if the username and password are correct
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    # if the username and password are correct, send a success message to the client
    if user:
        print("Login successful on server - sending success message to client")
        client.send("Login successful".encode())
    else:
        print("Login failed on server - sending failure message to client")
        client.send("Login failed".encode())


# handle register
def handle_register(client, data):
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
        client.send("Register failed".encode())
    else:
        # insert the user into the database
        c.execute("INSERT INTO users (first_name, last_name, email, username, password) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, email, username, password))
        conn.commit()
        print("Register successful on server - sending success message to client")
        client.send("Register successful".encode())


# get the tickets for the current user
def handle_get_user_tickets(client, username):
    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    try:
        # create a cursor
        c = conn.cursor()

        # get all user's transactions including event_id, total cost, and amount
        query = """SELECT concerts.event_name, transactions.total, transactions.amount 
                   FROM transactions 
                   JOIN concerts ON transactions.event_id = concerts.event_id
                   WHERE transactions.username = ?"""
        c.execute(query, (username,))
        tickets = c.fetchall()

        # Send the data to the client
        if tickets:
            # Convert list of tuples to a formatted string
            tickets_str = "\n".join(f"{event_name}, {total_cost}, {amount}" for event_name, total_cost, amount in tickets)
            client.send(tickets_str.encode())
            print("Sent user tickets to client:", tickets_str)
        else:
            print("User has no tickets")
            client.send("No tickets".encode())

    except sqlite3.Error as e:
        print("Database error:", e)
        client.send("Server error".encode())
    finally:
        conn.close()


# get all available concert tickets
def handle_get_tickets(client):
    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    # create a cursor
    c = conn.cursor()

    # get the first 15 concerts
    c.execute("SELECT * FROM concerts LIMIT 15")

    items = c.fetchall()
    # convert the list of tuples to a string to send to the client
    # else the program freezes and crashes
    str_items = str(items)

    client.send(str_items.encode())


# buy a ticket
def handle_buy_ticket(client, data):
    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    # create a cursor
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
            new_total = existing_ticket[4] + price
            c.execute("UPDATE transactions SET amount = ?, total = ? WHERE username = ? AND event_id = ?",
                      (new_amount, new_total, username, event_id))
        else:
            # add the ticket to the user's tickets
            c.execute("INSERT INTO transactions (username, event_id, amount, total, date) VALUES (?, ?, ?, ?, ?)",
                      (username, event_id, 1, price, date.today()))

        # update the user's funds
        c.execute("UPDATE users SET funds = ? WHERE username = ?", (funds, username))
        # subtract one from the amount of tickets available
        c.execute("UPDATE concerts SET amount = amount - 1 WHERE event_id = ?", (event_id,))

        conn.commit()
        print("Ticket purchased")
        client.send("Ticket purchased".encode())
    else:
        print("Insufficient funds")
        client.send("Insufficient funds".encode())

    conn.close()


# sell a ticket
def handle_sell_ticket(client, data):
    print("Received data:", data)
    # connect to sqlite database
    conn = sqlite3.connect(DB_PATH)
    # create a cursor
    c = conn.cursor()

    # split the data into event name and username (separated by a newline)
    event_name, username = data.split("\n", 1)

    # get the event_id of the ticket
    c.execute("SELECT event_id FROM concerts WHERE event_name = ?", (event_name,))
    event_id = c.fetchone()[0]
    print("Event ID:", event_id)

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
    print("Ticket sold")
    client.send("Ticket sold".encode())


# handle admin check - check if the user is an admin
def handle_admin_check(client, data):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # execute the query, data is a tuple with one element, so we need to add a comma after the element
        # sqlite expects a tuple (or list), even if there is only one element
        c.execute("SELECT admin FROM users WHERE username = ?", (data,))
        admin_status = c.fetchone()
        print("ADMIN STATUS_:", admin_status)
        if admin_status[0] == 1:
            response = "ADMIN"
            print("ADMIN STATUS RESPONSE:", response)
            client.send(response.encode())
        else:
            client.send("USER".encode())


def handle_get_currency(client, username):
    """Get the user's currency"""
    # connect to sqlite database
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT funds FROM users WHERE username = ?", (username,))
        funds = c.fetchone()[0]
        client.send(str(funds).encode())


def handle_logout(client):
    """Close the connection with the client"""
    client.close()



# Continuously listen for connections from clients
while True:
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

