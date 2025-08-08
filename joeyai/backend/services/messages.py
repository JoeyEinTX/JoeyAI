# Message service logic
from .db import get_conn

def list_messages(project_id, limit=200, order='asc'):
	c = get_conn()
	rows = c.execute(f'SELECT * FROM messages WHERE project_id=? ORDER BY ts {"ASC" if order=="asc" else "DESC"} LIMIT ?', (project_id, limit)).fetchall()
	return [dict(row) for row in rows]

def add_message(project_id, role, content):
	c = get_conn()
	c.execute('INSERT INTO messages (project_id, role, content) VALUES (?, ?, ?)', (project_id, role, content))
	mid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
	return dict(c.execute('SELECT * FROM messages WHERE id=?', (mid,)).fetchone())
