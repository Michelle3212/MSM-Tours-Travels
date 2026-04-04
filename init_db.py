import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# USERS (optional - you can keep or remove)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

# BOOKINGS (MAIN IMPORTANT TABLE)
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT,
package TEXT,
date TEXT,
message TEXT
)
""")

# MESSAGES (optional)
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
message TEXT
)
""")

# REVIEWS (optional)
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
review TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")