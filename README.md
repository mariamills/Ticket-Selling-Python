
# Ticket Selling

This application is a modern GUI-based ticket selling application for concert venues.

## Project Structure

```
project_root/
│
├── frames/
│   ├── login.py
│   ├── home.py
│   ├── register.py
│   └── 
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
│
├── main.py
└── 
```

- __frames/__: This directory contains all the frames for our application
- __network/__: This directory contains all the networking-related code
    - __client.py__: This file contains the client-side socket code
    - __server.py__: This file contains the server-side socket code
- __db/__: This directory contains all the database-related code
    - __projectDB.py__: This file contains the database code for table creation and insertion
- __main.py__: This is the main entry point for our application
