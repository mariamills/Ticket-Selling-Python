# TCP Server Socket
import socket
import threading
import sqlite3
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))
# path to the database - using the os module to get the path to the project directory, so it works on any machine
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'project.db')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
print("Server is ready to recieve")

def establish_connection(client):
    print("Connection established with client")
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
            case _:
                print("Invalid command")

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
        c.execute("INSERT INTO users (first_name, last_name, email, username, password) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, email, username, password))
        conn.commit()
        print("Register successful on server - sending success message to client")
        client.send("Register successful".encode())


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

