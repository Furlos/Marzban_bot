import os
from dotenv import load_dotenv


load_dotenv()



class Config:
    api_url = os.getenv("API_URL")
    admin_username = os.getenv("ADMIN_NAME")
    admin_password = os.getenv("ADMIN_PASS")


    @property
    def api_token(self):
        return os.getenv("API_TOKEN")


config_name = Config()