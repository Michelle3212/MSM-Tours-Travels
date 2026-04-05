import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT,
package TEXT,
start_date TEXT,
return_date TEXT,
message TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
review TEXT
)
""")

conn.commit()
conn.close()

print("Database updated successfully!")