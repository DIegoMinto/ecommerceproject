from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users(self):
        return self.repository.get_users()

    def register_user(self, username, email, password, rol):
        return self.repository.register_user(username, email, password, rol)

    def login_user(self, username, password):
        return self.repository.login_user(username, password)