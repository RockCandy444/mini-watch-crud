from monitor.backend.db import connect_db


def find_by_username(username):
    with connect_db() as conn:
        return conn.execute('SELECT id, username, password_hash FROM monitor_users WHERE username = %s', (username,)).fetchone()


def find_user(user_id):
    with connect_db() as conn:
        return conn.execute('SELECT id, username FROM monitor_users WHERE id = %s', (user_id,)).fetchone()


def create_user(username, password_hash):
    with connect_db() as conn:
        return conn.execute('INSERT INTO monitor_users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING RETURNING id', (username, password_hash)).fetchone()
