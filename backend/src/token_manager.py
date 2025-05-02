import os
from datetime import datetime
from typing import Optional
import httpx
from .config import config_name

class TokenManager:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self._current_token: Optional[str] = None

    async def manual_refresh(self):
        """Обновление токена при вводе /start"""
        try:
            print(f"[{datetime.now()}]Инициировано обновление токена")
            new_token = await self.generate_new_token()
            await self.update_env_token(new_token)
            self._current_token = new_token
            return True
        except httpx.HTTPStatusError as e:
            print(f"[{datetime.now()}] ошибка API при обновлении токена: {e.response.text}")
        except Exception as e:
            print(f"[{datetime.now()}] Критическая ошибка: {str(e)}")
        return False

    async def generate_new_token(self) -> str:
        """Генерирует новый токен через API Marzban"""
        url = f"{config_name.api_url.rstrip('/')}/api/admin/token"
        try:
            response = await self.client.post(
                url,
                data={
                    "username": config_name.admin_username,
                    "password": config_name.admin_password
                }
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error ({e.response.status_code}): {e.response.text}"
            print(f"Ошибка генерации токена: {error_msg}")
            raise
        except Exception as e:
            print(f"Неожиданная ошибка генерации токена: {str(e)}")
            raise

    @staticmethod
    async def update_env_token(new_token: str) -> None:
        """Безопасно обновляет токен в .env файле"""
        env_path = '.env'
        temp_path = f'{env_path}.tmp'

        try:
            # Читаем текущий файл
            lines = []
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    lines = f.readlines()

            # Обновляем или добавляем токен
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('API_TOKEN='):
                    lines[i] = f"API_TOKEN={new_token}\n"
                    updated = True
                    break

            if not updated:
                lines.append(f"API_TOKEN={new_token}\n")

            # Атомарная запись
            with open(temp_path, 'w') as f:
                f.writelines(lines)

            os.replace(temp_path, env_path)

            # Обновляем в памяти
            os.environ['API_TOKEN'] = new_token
            print(f"[{datetime.now()}] Токен обновлен в .env")

        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            print(f"[{datetime.now()}] Ошибка обновления .env: {str(e)}")
            raise

    async def close(self):
        """Корректное закрытие клиента"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class MarzbanAPIError(Exception):
    """Кастомное исключение для ошибок API"""
    pass