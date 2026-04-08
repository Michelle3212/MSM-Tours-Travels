import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT,
package TEXT,
start_date TEXT,
return_date TEXT,
message TEXT,
service TEXT
)
""")

conn.commit()
conn.close()

print("Fresh DB created!")