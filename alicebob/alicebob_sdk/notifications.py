import decouple
import requests
from pygments.lexer import default

PUSHOVER_TOKEN = decouple.config("PUSHOVER_TOKEN", default=None)
PUSHOVER_USER = decouple.config("PUSHOVER_USER", default=None)


class NotificationException(Exception):
    pass


def notify_pushover(title: str, message: str):
    """Send a notification to Pushover."""

    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_TOKEN,
                "user": PUSHOVER_USER,
                "title": title,
                "message": message,
            },
        )
    except Exception as e:
        raise NotificationException(e)


__all__ = ("notify_pushover", "NotificationException")

if __name__ == '__main__':
    notify_pushover("Test", "Test")
