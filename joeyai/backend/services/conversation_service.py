import sqlite3
from datetime import datetime
from joeyai.backend.services.db import get_db

def create_conversation(title=None):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO conversations (title) VALUES (?)", (title,))
    db.commit()
    id = cur.lastrowid
    cur.execute("SELECT id, title, created_at, updated_at FROM conversations WHERE id=?", (id,))
    return dict(cur.fetchone())

def list_conversations(limit=50):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, updated_at FROM conversations ORDER BY updated_at DESC LIMIT ?", (limit,))
    return [dict(row) for row in cur.fetchall()]

def rename_conversation(id, title):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE conversations SET title=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (title, id))
    db.commit()
    cur.execute("SELECT id, title, created_at, updated_at FROM conversations WHERE id=?", (id,))
    return dict(cur.fetchone())

def get_messages(conversation_id, limit=500):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, role, content, ts FROM messages WHERE conversation_id=? ORDER BY ts ASC LIMIT ?", (conversation_id, limit))
    return [dict(row) for row in cur.fetchall()]

def add_message(conversation_id, role, content):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)", (conversation_id, role, content))
    db.commit()
    cur.execute("UPDATE conversations SET updated_at=CURRENT_TIMESTAMP WHERE id=?", (conversation_id,))
    cur.execute("SELECT id, role, content, ts FROM messages WHERE id=?", (cur.lastrowid,))
    return dict(cur.fetchone())

def ensure_tables():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        role TEXT CHECK(role IN ('user','assistant')),
        content TEXT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(conversation_id) REFERENCES conversations(id)
    )
    """)
    db.commit()
