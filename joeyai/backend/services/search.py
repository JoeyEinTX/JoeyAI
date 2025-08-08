from .db import get_conn

def search_messages(q, limit=100):
	c = get_conn()
	rows = c.execute('''
		SELECT m.project_id, m.id, snippet(messages_fts, 0, '<b>', '</b>', '...', 10) as snippet, m.ts
		FROM messages_fts
		JOIN messages m ON m.id = messages_fts.rowid
		WHERE messages_fts MATCH ?
		ORDER BY m.ts DESC
		LIMIT ?
	''', (q, limit)).fetchall()
	return [dict(row) for row in rows]
