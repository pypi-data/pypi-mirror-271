import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id="

    def send_message(self, chat_id, message):
        url = self.base_url + f"{chat_id}&text={message}"
        response = requests.get(url)
        return response.json()
