import requests
import os

BOT = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]


def send(msg):

    requests.post(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        json={
            "chat_id": CHAT,
            "text": msg
        }
    )
