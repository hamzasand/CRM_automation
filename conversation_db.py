import sqlite3
import os

DB_FILE = "conversations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS threads (
            email TEXT,
            thread TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_conversation(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT thread FROM threads WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    return eval(result[0]) if result else []

def update_conversation(email, messages):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("REPLACE INTO threads (email, thread) VALUES (?, ?)", (email, str(messages)))
    conn.commit()
    conn.close()
