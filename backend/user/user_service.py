import requests
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from backend.settings.config import api_token, api_url


class MarzbanAPIError(Exception):
    """Класс для ошибок API Marzban"""
    pass


class UserService:
    def __init__(self, api_url: str, api_token: str):
        """
        Инициализация сервиса для работы с пользователями VPN.

        :param api_url: URL API Marzban (например, 'https://vpn.example.com/api')
        :param api_token: API Token администратора Marzban
        """
        self.api_url = api_url.rstrip('/')
        self.api_token = api_token

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Внутренний метод для выполнения запросов к API

        :param method: HTTP метод (GET, POST, PUT)
        :param endpoint: Конечная точка API
        :param data: Данные для отправки
        :return: Ответ API в виде словаря
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            else:
                raise MarzbanAPIError(f"Неверный HTTP метод: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка при выполнении запроса к Marzban API: {str(e)}"
            if e.response is not None:
                error_msg += f", статус: {e.response.status_code}, ответ: {e.response.text}"
            raise MarzbanAPIError(error_msg)

    def _generate_ss_link(self, method: str, password: str, server: str, port: int, username: str) -> str:
        """
        Генерация ссылки для подключения Shadowsocks

        :param method: Метод шифрования
        :param password: Пароль
        :param server: Адрес сервера
        :param port: Порт
        :param username: Имя пользователя
        :return: Ссылка для подключения в формате ss://
        """
        ss_config = f"{method}:{password}@{server}:{port}"
        ss_config_encoded = base64.urlsafe_b64encode(ss_config.encode()).decode()
        return f"ss://{ss_config_encoded}#{username}"

    def create_user(self, telegram_id: str, limit_traffic_gb: float, expire_days: int) -> Dict[str, Any]:
        """
        Создает нового пользователя VPN

        :param telegram_id: ID пользователя в Telegram
        :param limit_traffic_gb: Лимит трафика в гигабайтах
        :param expire_days: Срок действия в днях
        :return: Данные созданного пользователя
        """
        # 1. Подготовка данных
        expire_date = datetime.now() + timedelta(days=expire_days)
        expire_timestamp = int(expire_date.timestamp())

        # 2. Формируем user_data
        user_data = {
            "username": str(telegram_id),
            "proxies": {
                "shadowsocks": {
                    "method": "chacha20-ietf-poly1305",
                }
            },
            "inbounds": {
                "shadowsocks": []  # Автоматический выбор доступного inbound
            },
            "expire": expire_timestamp,
            "data_limit": limit_traffic_gb * 1024 * 1024 * 1024,  # Конвертация GB → bytes
            "data_limit_reset_strategy": "month"  # Автосброс трафика
        }

        # 3. Отправка запроса
        response = self._make_request("POST", "/api/user", user_data)

        # 4. Обработка ответа
        ss_config = response.get("proxies", {}).get("shadowsocks", {})

        # Получаем адрес сервера (если не указан, используем домен из API URL)
        server = ss_config.get("server") or self.api_url.split('//')[-1].split('/')[0]

        # Формируем ссылку для подключения
        connection_link = self._generate_ss_link(
            method=ss_config.get("method", "chacha20-ietf-poly1305"),
            password=ss_config.get("password", ""),
            server=server,
            port=ss_config.get("port", 443),
            username=response.get("username", "")
        )

        # 5. Возвращаем структурированные данные
        return {
            "username": response.get("username"),
            "expire_date": expire_date.strftime("%Y-%m-%d"),
            "data_limit_gb": limit_traffic_gb,
            "connection_link": connection_link,
        }

    def update_user(self, telegram_id: str, limit_traffic_gb: Optional[float] = None,
                    expire_days: Optional[int] = None) -> Dict[str, Any]:
        """
        Обновление данных пользователя VPN

        :param telegram_id: ID пользователя Telegram (username)
        :param limit_traffic_gb: Новый лимит трафика в GB (None если не нужно менять)
        :param expire_days: Количество дней до истечения срока действия (None если не нужно менять)
        :return: Информация об обновленном пользователе
        """
        # Получаем текущие данные пользователя
        try:
            current_user = self._make_request("GET", f"/api/user/{telegram_id}")
        except MarzbanAPIError as e:
            if "status: 404" in str(e):
                raise MarzbanAPIError(f"Пользователь с ID {telegram_id} не найден")
            raise

        # Подготавливаем данные для обновления
        update_data = {}

        if expire_days is not None:
            current_expire = current_user.get("expire", 0)
            now_timestamp = int(datetime.now().timestamp())

            if current_expire < now_timestamp:
                new_expire = datetime.now() + timedelta(days=expire_days)
            else:
                current_expire_date = datetime.fromtimestamp(current_expire)
                new_expire = current_expire_date + timedelta(days=expire_days)

            update_data["expire"] = int(new_expire.timestamp())

        if limit_traffic_gb is not None:
            update_data["data_limit"] = limit_traffic_gb * 1024 * 1024 * 1024

        # Если есть что обновлять, выполняем запрос
        if update_data:
            updated_user = self._make_request("PUT", f"/api/user/{telegram_id}", update_data)
            return {
                "username": updated_user["username"],
                "expire_date": datetime.fromtimestamp(updated_user["expire"]).strftime("%Y-%m-%d"),
                "data_limit_gb": updated_user["data_limit"] / (1024 ** 3) if updated_user["data_limit"] else 0
            }

        return {
            "username": current_user["username"],
            "expire_date": datetime.fromtimestamp(current_user["expire"]).strftime("%Y-%m-%d"),
            "data_limit_gb": current_user["data_limit"] / (1024 ** 3) if current_user["data_limit"] else 0
        }

    def get_user(self, telegram_id: str) -> Dict[str, Any]:
        """
        Получение информации о пользователе

        :param telegram_id: ID пользователя Telegram (username)
        :return: Информация о пользователе
        """
        user_data = self._make_request("GET", f"/api/user/{telegram_id}")
        return {
            "username": user_data["username"],
            "expire_date": datetime.fromtimestamp(user_data["expire"]).strftime("%Y-%m-%d"),
            "data_limit_gb": user_data["data_limit"] / (1024 ** 3) if user_data["data_limit"] else 0,
            "used_traffic_gb": user_data["used_traffic"] / (1024 ** 3) if user_data["used_traffic"] else 0,
            "status": user_data["status"]
        }