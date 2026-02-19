import requests
from config import TELEGRAM_TOKEN, CHAT_ID


def send(message: str) -> bool:
    """
    Send message to Telegram bot.
    Returns True on success, False on failure.
    Splits long messages automatically (Telegram limit: 4096 chars).
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    # split into chunks of 4000 chars to be safe
    chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]

    success = True
    for chunk in chunks:
        try:
            r = requests.post(url, data={
                "chat_id": CHAT_ID,
                "text": chunk,
                "parse_mode": "HTML"
            }, timeout=10)

            if not r.ok:
                print(f"[Telegram] Failed: {r.text}")
                success = False

        except Exception as e:
            print(f"[Telegram] Error: {e}")
            success = False

    return success