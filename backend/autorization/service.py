class AutorizationService:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def autorize(self, username: str, password: str):
        return "Token"
        # Запрос в марзбан на авторизацию админа в начале requests(https://instant-paris.space/api/admin/token, self.username, self.password)
