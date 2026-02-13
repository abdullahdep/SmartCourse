import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np

# Configure SQLite for better concurrent access on Windows
sqlite3.connect("smartcourse.db").execute("PRAGMA journal_mode=WAL").close()

def convert_nan_to_none(obj):
    """Recursively convert NaN values to None for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_nan_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_nan_to_none(item) for item in obj]
    elif isinstance(obj, float) and np.isnan(obj):
        return None
    return obj

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
        c.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course_title TEXT,
                course_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, course_title)
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
        
        # Clean up corrupted NaN values in history
        c.execute("SELECT id, results FROM history WHERE results LIKE '%NaN%' OR results LIKE '%nan%'")
        corrupted_entries = c.fetchall()
        for entry_id, results_str in corrupted_entries:
            try:
                # Replace NaN with null and re-save
                cleaned = results_str.replace('NaN', 'null').replace('nan', 'null')
                c.execute("UPDATE history SET results = ? WHERE id = ?", (cleaned, entry_id))
            except Exception as e:
                print(f"Warning: Could not clean history entry {entry_id}: {str(e)}")
        if corrupted_entries:
            conn.commit()
            print(f"Cleaned {len(corrupted_entries)} corrupted history entries")
            
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
        # Clean NaN values before saving
        cleaned_results = convert_nan_to_none(results)
        c.execute("INSERT INTO history (user_id, query, model, results) VALUES (?, ?, ?, ?)",
                  (user_id, query, model, json.dumps(cleaned_results)))
        conn.commit()
    finally:
        conn.close()

def get_history(user_id=None):
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        if user_id:
            c.execute("SELECT id, query, model, results, timestamp FROM history WHERE user_id = ? ORDER BY id DESC", (user_id,))
        else:
            c.execute("SELECT id, query, model, results, timestamp FROM history ORDER BY id DESC")
        data = c.fetchall()
        result = []
        for row in data:
            try:
                # Try to parse results as JSON
                results_data = row[3]
                if isinstance(results_data, str):
                    # Try to parse, but handle NaN by replacing with null
                    results_data = results_data.replace('NaN', 'null').replace('nan', 'null')
                    results_data = json.loads(results_data)
                
                result.append({
                    "query": row[1],
                    "model": row[2],
                    "results": results_data,
                    "timestamp": row[4]
                })
            except (json.JSONDecodeError, ValueError) as e:
                # Skip corrupted entries
                print(f"Warning: Skipping corrupted history entry {row[0]}: {str(e)}")
                continue
        return result
    finally:
        conn.close()

def save_favorite(user_id, course_title, course_data):
    """Save a course to user's favorites"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("INSERT INTO favorites (user_id, course_title, course_data) VALUES (?, ?, ?)",
                  (user_id, course_title, json.dumps(course_data)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Course already favorited
        return False
    finally:
        conn.close()

def get_favorites(user_id):
    """Get all favorite courses for a user"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("SELECT course_title, course_data, timestamp FROM favorites WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        data = c.fetchall()
        result = []
        for row in data:
            result.append({
                "title": row[0],
                "data": json.loads(row[1]),
                "timestamp": row[2]
            })
        return result
    finally:
        conn.close()

def delete_favorite(user_id, course_title):
    """Remove a course from user's favorites"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("DELETE FROM favorites WHERE user_id = ? AND course_title = ?", (user_id, course_title))
        conn.commit()
        return True
    finally:
        conn.close()

def is_favorite(user_id, course_title):
    """Check if a course is favorited by user"""
    conn = sqlite3.connect("smartcourse.db", timeout=10)
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM favorites WHERE user_id = ? AND course_title = ?", (user_id, course_title))
        return c.fetchone() is not None
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