import sqlite3
import json

def init_db():
    conn = sqlite3.connect("smartcourse.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            model TEXT,
            results TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_history(query, model, results):
    conn = sqlite3.connect("smartcourse.db")
    c = conn.cursor()
    c.execute("INSERT INTO history (query, model, results) VALUES (?, ?, ?)",
              (query, model, json.dumps(results)))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect("smartcourse.db")
    c = conn.cursor()
    c.execute("SELECT query, model, results, timestamp FROM history ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data
