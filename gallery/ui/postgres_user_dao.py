from .db import get_secret, get_password, get_host, get_username, get_dbname, connect, execute
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    def get_users(self):
        result = []
        cursor = db.execute("select username,password,full_name from users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
        return result

    def delete_user(self, username):
        db.execute("delete from users where username=%s", (username,))