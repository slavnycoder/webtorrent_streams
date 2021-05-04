from cent import Client

from backend.settings import CENTRIFUGO

cent_client = Client(f"http://{CENTRIFUGO['host']}/", api_key=CENTRIFUGO["api_key"], timeout=1)
