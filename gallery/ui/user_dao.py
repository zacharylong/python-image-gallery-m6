class UserDAO:

    def get_users(self):
        raise Exception("Must be implemented")

    def delete_user(self, username):
        raise Exception("Must be implemented")

    def get_user_by_username(self, username):
        raise Exception("Must be implemented")