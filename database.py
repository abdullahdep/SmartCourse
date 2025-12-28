import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Configure SQLite for better concurrent access on Windows
sqlite3.connect("smartcourse.db").execute("PRAGMA journal_mode=WAL").close()

def init_db():
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                model TEXT,
                results TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        
        # Create test user if it doesn't exist
        c.execute("SELECT * FROM users WHERE username = ?", ("test",))
        if not c.fetchone():
            hashed_pwd = generate_password_hash("test@1234")
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     ("test", "test@example.com", hashed_pwd))
            conn.commit()
            
    finally:
        conn.close()

def create_user(username, email, password):
    """Register a new user"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Username or email already exists
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials and return user info if valid"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("SELECT id, username, email, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        
        if user and check_password_hash(user[3], password):
            return {"id": user[0], "username": user[1], "email": user[2]}
        return None
    finally:
        conn.close()

def get_user(user_id):
    """Get user by ID"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        
        if user:
            return {"id": user[0], "username": user[1], "email": user[2]}
        return None
    finally:
        conn.close()

def save_history(user_id, query, model, results):
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("INSERT INTO history (user_id, query, model, results) VALUES (?, ?, ?, ?)",
                  (user_id, query, model, json.dumps(results)))
        conn.commit()
    finally:
        conn.close()

def get_history(user_id=None):
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        if user_id:
            c.execute("SELECT query, model, results, timestamp FROM history WHERE user_id = ? ORDER BY id DESC", (user_id,))
        else:
            c.execute("SELECT query, model, results, timestamp FROM history ORDER BY id DESC")
        data = c.fetchall()
        return data
    finally:
        conn.close()
# Admin authentication
ADMIN_USERNAME = "Iqra"
ADMIN_PASSWORD_HASH = generate_password_hash("Iqra@1234")

def verify_admin(username, password):
    """Verify admin credentials"""
    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        return True
    return False

def get_admin_token():
    """Generate a simple admin token (not JWT, just a simple string for admin session)"""
    import hashlib
    import time
    token_data = f"{ADMIN_USERNAME}:{int(time.time())}"
    return hashlib.sha256(token_data.encode()).hexdigest()