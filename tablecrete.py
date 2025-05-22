import sqlite3

conn = sqlite3.connect('d:/zxfsDGzfdsh/google_drive_gallery_full/users.db')  # path को सही रखें
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ Database और users टेबल बन चुकी है!")
