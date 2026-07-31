import json
import os
import requests

from config import (
    BOT_TOKEN,
    CHAT_ID,
    SENT_FILE,
)


# --------------------------------
# Load sent products
# --------------------------------
def load_sent():

    if not os.path.exists(SENT_FILE):
        return []

    try:
        with open(SENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# --------------------------------
# Save sent products
# --------------------------------
def save_sent(sent):

    with open(SENT_FILE, "w") as f:
        json.dump(sent, f, indent=4)


# --------------------------------
# Send Telegram message
# --------------------------------
def send_message(text):

    if BOT_TOKEN == "" or CHAT_ID == "":
        print("Telegram not configured.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }

    try:

        r = requests.post(
            url,
            data=payload,
            timeout=30,
        )

        r.raise_for_status()

    except Exception as e:
        print("Telegram Error:", e)


# --------------------------------
# Notify only new products
# --------------------------------
def notify(products):

    sent = load_sent()

    changed = False

    for product in products:

        product_id = product["productCode"]

        if product_id in sent:
            continue

        sent.append(product_id)
        changed = True

        price = int(float(product["finalPrice"]))

        message = f"""
🔥 Lenovo Outlet Match Found!

💻 {product['productName']}

💰 ₹{price:,}

🔗 https://www.lenovo.com{product['url']}
"""

        send_message(message.strip())

    if changed:
        save_sent(sent)
