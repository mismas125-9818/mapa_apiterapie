import sqlite3

conn = sqlite3.connect('databaza.db')
cur = conn.cursor()

# Vytvorenie tabuľky s podporou fotiek a jazyka
cur.execute('''
CREATE TABLE IF NOT EXISTS helpers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meno TEXT,
    odbor TEXT,
    lat REAL,
    lng REAL,
    telefon TEXT,
    email TEXT,
    foto TEXT,
    adresa TEXT,
    jazyk TEXT
)
''')

# Príklad záznamu
cur.execute('''
INSERT INTO helpers (meno, odbor, lat, lng, telefon, email, foto, adresa, jazyk)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', ("Ján", "oprava notebookov", 48.146, 17.107, "+421900123456", "jan@example.com", "jan.jpg", "Bratislava, Slovakia", "slovenčina"))

conn.commit()
conn.close()
print("Databáza pripravená ✅")
