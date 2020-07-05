from .user_admin_m3 import get_secret_image_gallery, get_password, get_host, get_username, get_dbname, connect, execute
from .user import User
from .user_dao import UserDAO
import user_admin_m3

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    def get_users(self):
        result = []
        cursor = user_admin_m3.execute("select username,password,full_name from users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
        return result

    def delete_user(self, username):
        user_admin_m3.execute("delete from users where username=%s", (username,))