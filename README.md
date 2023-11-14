
# Ticket Selling Application

Welcome to this **Ticket Selling Application** repository! This application is a modern, GUI-based platform designed for users to buy and sell tickets for concert venues. It also contains an **admin dashboard** for *admins user* to manage ticket inventories through create, update, and delete operations.

As an **educational project**, this application **intentionally incorporates certain vulnerabilities** to highlight the critical role of security in software development and to serve as a learning tool for secure coding practices.

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Features](#features)
- [User Guide](#user-guide)
  - [How to Run](#how-to-run)
  - [Video Demo](#video-demo)
- [Learnings](#learnings)
- [Vulnerabilities](#vulnerabilities)
- [Preventing Vulnerabilities](#preventing-vulnerabilities)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Tools](#tools)
- [License](#license)


## Introduction

This application simulates a ticket selling system with a focus on user interaction and network communication. It is built using Python and CustomTkinter for an enhanced user interface, SQLite3 for database management, and TCP socket programming for network operations.

## Project Structure
```
project_root/
│
├── frames/
│   ├── add_tickets.py
│   ├── admin.py
│   ├── buy_tickets.py
│   ├── home.py
│   ├── login.py
│   ├── register.py
│   └── view_tickets.py
│
├── network/
│   ├── __init__.py
│   ├── client.py
│   └── server.py
│
├── db/
│   ├── __init__.py
│   └── projectDB.py
│
├── main.py
├── README.md
├── requirements.txt
└── TODO.md
```

- __frames/__: This directory contains all the frames for our application
- __network/__: This directory contains all the networking-related code
    - __client.py__: This file contains the client-side socket code
    - __server.py__: This file contains the server-side socket code
- __db/__: This directory contains all the database-related code
    - __projectDB.py__: This file contains the database code for table creation and insertion
- __main.py__: This is the main entry point for our application
- __TODO.md__: This file contains a list of tasks that need to be completed, bugs that need to be fixed, and any additional potential features or improvements that can be made

## Features
- **User Registration and Authentication**: Secure sign-up and login system for users.
- **Ticket Management**: Users can buy and sell tickets, while admins can create, update, and delete ticket listings.
- **Real-time Networking**: Persistent socket-based client-server architecture for real-time updates.
- **Interactive GUI**: CustomTkinter widgets provide a modern and responsive user interface.
- **Security Demonstrations**: The application includes examples of common vulnerabilities to serve as a learning tool for secure coding.

# User Guide

## How to Run
To set up the application, ensure you have Python installed on your system. 

1. Clone the repository
2. Navigate to the project directory:
```bash
cd ticket-selling-python <or whatever you named the directory>
```
3. and install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Create the database by either:
    - Running the `projectDB.py` file in the `db` directory
    - OR Running the `projectDB.sql` file in the `db` directory in a SQL editor (If you've set up your own database)
5. Run the server:
```bash
python server.py
```
6. Run the application:
```bash
python main.py
```
The GUI should pop up, and you can start using the application! 

Register an account or execute the included SQL script and use any of the following credentials to log in:
- Username: `john` Password: `doe123` (Regular User)
- Username: `admin` Password: `admin` (Admin User)
  -  **Yes, these account DO NOT meet the password requirements, but they are included for testing purposes. So they're made for convenience.**

## Video Demo
To be added.

## Learnings
Throughout the development of this application, we've gained invaluable insights into various aspects of software engineering and defensive programming. Here's a highlight of our key learnings:

- **Context Managers for Database Connections**: We've leveraged Python's context managers to handle database connections, ensuring efficient resource management and error handling, which is crucial for maintaining the application's performance and reliability.

- **Prepared Statements for SQL Queries**: Our use of prepared statements has fortified our application against SQL injection attacks, showcasing the importance of secure coding practices when dealing with user inputs and database interactions.

- **Socket Communication**: The transition from multiple transient client sockets to a single persistent socket connection has been a significant learning curve, emphasizing the efficiency and security benefits of maintaining a stable communication channel in networked applications.

- **Password Hashing and Salting**: We've explored the mechanisms of password security, understanding how hashing and salting protect user credentials, a fundamental aspect of secure authentication.

- **TCP Encryption**: The exploration of TCP encryption highlighted the necessity of securing data in transit, a critical consideration in the prevention of eavesdropping and man-in-the-middle attacks.

- **SQL Injection**: Delving into the vulnerabilities of SQL injection has been a practical lesson in database security and the importance of validating and sanitizing user inputs.

- **Comprehensive Python Refresher**: The project served as an extensive refresher on Python programming, covering a wide range of its capabilities and libraries.

- **Python Unit Testing**: We've learned to ensure code reliability and functionality through unit testing, an essential practice for any robust software development process.

- **CustomTkinter Library**: The use of CustomTkinter has provided us with a deeper understanding of GUI development, enhancing the user experience with a modern look and feel.

- **Client-Server Architecture**: Building a client-server architecture from scratch has given us hands-on experience with this fundamental networking model.

- **Database Interaction**: We've honed our skills in database manipulation, from schema design to CRUD operations, data retrieval, and more using SQLite3.

- **GUI Development**: The creation of a user-friendly interface has taught us the intricacies of GUI design and user interaction flows.

- **Enhanced SQL**: We've improved our SQL skills, learning to write more complex queries and understanding the performance implications of various database operations.

## Vulnerabilities
Our application intentionally includes two vulnerabilities to serve as a teaching tool:

- **Plaintext Passwords**: Storing passwords in plaintext poses a significant risk, as it allows anyone with database access to read user credentials.

- **SQL Injection**: The application's initial susceptibility to SQL injection attacks could allow attackers to manipulate or corrupt the database.

- **Unencrypted TCP Traffic**: Initially, our TCP traffic was unencrypted, making it vulnerable to interception and unauthorized access through programs like Wireshark.

## Preventing Vulnerabilities
To combat these vulnerabilities, we've implemented several security measures:

- **Password Hashing and Salting**: We now use hashing and salting to store passwords securely, transforming them into indecipherable hashes that are resistant to brute-force attacks by using the library `bcrypt` to hash and salt the passwords.

- **Prepared Statements**: By using prepared statements, we've eliminated the risk of SQL injection, ensuring that user inputs are treated as data, not executable code. Prepared statements do this by separating the SQL logic from the user input, and then binding the user input to the SQL logic, **which prevents the user input from being executed as SQL code.**

- **TCP Encryption with TLS**: Implementing TLS has encrypted our TCP traffic, safeguarding data transmission against eavesdropping and ensuring the confidentiality and integrity of user data over the network.

## Screenshots
To be added.

## Contributing
We welcome contributions and suggestions! Please feel free to fork the repository, make changes, and submit pull requests. You can also open an issue for bugs, suggestions, or discussions.

## Tools
- [Python Socket Programming](https://realpython.com/python-sockets/)
- [Custom Tkinter Widgets](https://github.com/TomSchimansky/CustomTkinter)
- [CTkMessageBox](https://github.com/Akascape/CTkMessagebox/tree/main)

## License
This project is licensed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license.
- We chose the MIT license because it is a permissive license that is short and to the point. It lets people do anything they want with our code as long as they provide attribution back to us and don’t hold us liable. 
- Being that this is an educational project, we want to make it as easy as possible for people to use our code for their own learning purposes.

---
