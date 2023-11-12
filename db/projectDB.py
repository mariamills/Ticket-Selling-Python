import sqlite3

conn = sqlite3.connect('project.db')
c = conn.cursor()

# Drop users table if it exists
c.execute("DROP TABLE IF EXISTS users")

# Drop concerts table if it exists
c.execute("DROP TABLE IF EXISTS concerts")

c.execute(""" 
CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          email TEXT NOT NULL,
          username TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL,
          funds REAL NOT NULL DEFAULT 500.00,
          admin INTEGER NOT NULL DEFAULT 0
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS concerts(
          event_id INTEGER PRIMARY KEY AUTOINCREMENT,
          event_name TEXT,
          price REAL,
          amount INTEGER,
          date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transactions(
          transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT,
          event_id INTEGER,
          amount INTEGER,
          total REAL,
          date TEXT,
          FOREIGN KEY (username) REFERENCES users (username)
)
""")

# Users
c.execute("INSERT INTO users (first_name, last_name, email, username, password, admin) VALUES (?, ?, ?, ?, ?, ?)",
          ('admin', 'admin', 'admin@admin.com', 'admin', 'admin', 1))

c.execute("INSERT INTO users (first_name, last_name, email, username, password) VALUES (?, ?, ?, ?, ?)",
          ('john', 'doe', 'john@doe.com', 'john', 'doe123'))


# Tickets
c.execute("INSERT INTO concerts (event_name, price, amount, date) VALUES (?, ?, ?, ?)",
            ('The Weeknd', 100.00, 100, '2021-10-01'))

c.execute("INSERT INTO concerts (event_name, price, amount, date) VALUES (?, ?, ?, ?)",
            ('Kanye West', 200.00, 100, '2021-10-02'))

c.execute("INSERT INTO concerts (event_name, price, amount, date) VALUES (?, ?, ?, ?)",
            ('Drake', 300.00, 100, '2021-10-03'))

c.execute("INSERT INTO concerts (event_name, price, amount, date) VALUES (?, ?, ?, ?)",
            ('Ariana Grande', 400.00, 100, '2021-10-04'))

c.execute("SELECT * FROM users")
rows = c.fetchall()
for row in rows:
    print(row)

c.execute("SELECT * FROM concerts")
rows = c.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()