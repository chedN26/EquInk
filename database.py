import sqlite3

DB_PATH = "uploads.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_type TEXT,
            color REAL,
            blk REAL,
            cost INTEGER,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_upload(file_name, file_type, color, blk, cost):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO uploads (file_name, file_type, color, blk, cost)
        VALUES (?, ?, ?, ?, ?)
    ''', (file_name, file_type, color, blk, cost))
    conn.commit()
    conn.close()

def get_upload_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, file_name, file_type, color, blk, cost, upload_time
        FROM uploads
        ORDER BY upload_time DESC
    ''')
    rows = c.fetchall()
    conn.close()
    return rows
