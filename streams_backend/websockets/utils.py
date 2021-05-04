import jwt
from cent import Client

from backend import settings


def create_ws_token(username: str):
    return jwt.encode({"sub": username}, settings.CENTRIFUGO["secret"], algorithm="HS256").decode()


def presence_stats(client: Client, channel: str):
    client.add("presence_stats", {
        "channel": channel
    })
    result = client.send()
    return result[0]
