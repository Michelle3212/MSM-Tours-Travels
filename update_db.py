import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("ALTER TABLE bookings ADD COLUMN service TEXT")
conn.commit()
conn.close()

print("Column added!")