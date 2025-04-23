from backend.autorization.service import AutorizationService


class AdminService(AutorizationService):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token = AutorizationService.autorize(self.username, self.password)

    def create(
        self,
        username: str,
        password: str,
    ):
        return self.username
        # Запрос в марзбан на создание админа
