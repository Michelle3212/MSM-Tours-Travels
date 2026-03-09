import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

conn.execute("""
CREATE TABLE bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
package TEXT,
date TEXT
)
""")

conn.execute("""
CREATE TABLE messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
message TEXT
)
""")

conn.commit()
conn.close()

print("Database created!")