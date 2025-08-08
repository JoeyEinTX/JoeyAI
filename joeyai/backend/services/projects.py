# Project service logic
from .db import get_conn

def list_projects(limit=100):
	c = get_conn()
	rows = c.execute('SELECT * FROM projects ORDER BY updated_at DESC LIMIT ?', (limit,)).fetchall()
	return [dict(row) for row in rows]

def create_project(title=None):
	c = get_conn()
	c.execute('INSERT INTO projects (title) VALUES (?)', (title,))
	pid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
	return dict(c.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone())

def rename_project(id, title):
	c = get_conn()
	c.execute('UPDATE projects SET title=?, updated_at=CURRENT_TIMESTAMP WHERE id=?', (title, id))
	return dict(c.execute('SELECT * FROM projects WHERE id=?', (id,)).fetchone())

def delete_project(id):
	c = get_conn()
	c.execute('DELETE FROM messages WHERE project_id=?', (id,))
	c.execute('DELETE FROM projects WHERE id=?', (id,))
	return {"ok": True}
