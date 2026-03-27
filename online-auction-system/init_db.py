import sqlite3

db = sqlite3.connect("database.db")

db.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

db.execute("""
CREATE TABLE auctions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price INTEGER,
    end_time TEXT
)
""")

db.commit()
db.close()

print("Database created!")