"""Telegram bot's internal service configuration."""
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
url = os.getenv("API_URL", "http://backend:3000").rstrip("/")
internal_api_key = os.getenv("INTERNAL_API_KEY", "")
