import io
import json

import requests
from django.core.management.base import BaseCommand

from file_storages.google_cloud import gs_client, gs_emoticons_map_path

FETCH_EMOTICONS_NUMBER = 1000
PAGE_SIZE = 200


class Command(BaseCommand):
    help = "Fetch emoticons data"

    def handle(self, *args, **options):
        emoticons = {}
        for i in range(int(FETCH_EMOTICONS_NUMBER / PAGE_SIZE)):
            r = requests.get(f"http://api.frankerfacez.com/v1/emoticons?sort=count-desc&per_page={PAGE_SIZE}&page={i + 1}")
            response_data = json.loads(r.content.decode())
            for emo in response_data["emoticons"]:
                emo_name = emo["name"]
                if not emoticons.get(emo_name) or (emoticons.get(emo_name) and emo["usage_count"] > emoticons[emo_name]["count"]):
                    emoticons[emo_name] = dict(url=emo["urls"]["1"].split(".com/")[-1], count=emo["usage_count"])
        with io.StringIO(json.dumps(emoticons, separators=(',', ':'))) as map_file:
            gs_client.upload_file(map_file, gs_emoticons_map_path(), content_type="application/json")
