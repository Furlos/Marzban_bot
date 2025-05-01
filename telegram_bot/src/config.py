import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("BOT_TOKEN")
url = os.getenv("API_URL")