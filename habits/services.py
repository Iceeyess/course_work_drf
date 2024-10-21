import requests
from config import settings


def send_tg_message(chat_id: int, message: str) -> None:
    """Отправляет сообщение пользователю в телеграм"""
    method = 'sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    url = settings.TG_API_LINK + settings.TG_BOT_TOKEN + '/' + method
    requests.get(url, params=params)
