#!/usr/bin/env python
import sqlite3
import json
from database import init_db, save_history, get_history, create_user, verify_user

# Initialize database
print("Initializing database...")
init_db()

# Check if database exists
try:
    conn = sqlite3.connect("smartcourse.db")
    c = conn.cursor()
    
    # Check users table
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    print(f"Users in database: {user_count}")
    
    # Check history table
    c.execute("SELECT COUNT(*) FROM history")
    history_count = c.fetchone()[0]
    print(f"History entries: {history_count}")
    
    # Get all users
    c.execute("SELECT id, username FROM users")
    users = c.fetchall()
    print(f"Users list: {users}")
    
    # Test adding history
    if users:
        user_id = users[0][0]
        test_results = [
            {"courseoffered": "Python Basics", "department": "CS", "title": "MIT", "score": 95.5},
            {"courseoffered": "Data Science", "department": "CS", "title": "Stanford", "score": 87.3}
        ]
        
        print(f"\nTesting save_history for user {user_id}...")
        save_history(user_id, "test query", "both", {"tfidf": test_results, "neural": test_results})
        
        # Check if it was saved
        c.execute("SELECT COUNT(*) FROM history")
        history_count = c.fetchone()[0]
        print(f"History entries after save: {history_count}")
        
        # Get history
        history = get_history(user_id)
        print(f"Retrieved history: {len(history)} entries")
        if history:
            for h in history:
                print(f"  Query: {h[0]}, Model: {h[1]}, Timestamp: {h[3]}")
    
    conn.close()
    print("\n✅ Database test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
