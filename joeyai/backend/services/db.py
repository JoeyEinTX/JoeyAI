import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'joeyai.db'

conn = None

def get_conn():
	global conn
	if conn is None:
		conn = sqlite3.connect(DB_PATH, check_same_thread=False, isolation_level=None)
		conn.row_factory = sqlite3.Row
		conn.execute('PRAGMA journal_mode=WAL;')
	return conn

def init():
	c = get_conn()
	c.executescript('''
	CREATE TABLE IF NOT EXISTS projects (
		id INTEGER PRIMARY KEY,
		title TEXT,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
	);
	CREATE TABLE IF NOT EXISTS messages (
		id INTEGER PRIMARY KEY,
		project_id INTEGER,
		role TEXT CHECK(role IN ("user","assistant")),
		content TEXT,
		ts DATETIME DEFAULT CURRENT_TIMESTAMP
	);
	CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(content, content='messages', content_rowid='id');
	CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
		INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
	END;
	CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
		UPDATE messages_fts SET content = new.content WHERE rowid = new.id;
	END;
	CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
		DELETE FROM messages_fts WHERE rowid = old.id;
	END;
	''')
import sqlite3
# SQLite + FTS5 setup will go here
