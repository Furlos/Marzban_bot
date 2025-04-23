from backend.autorization.service import AutorizationService


class UserService(AutorizationService):
    def __init__(self, username: str, password: str, token):
        self.username = username
        self.password = password
        self.token = token

    def create(self, username):
        pass

    def restart_sub(self, username):
        pass
