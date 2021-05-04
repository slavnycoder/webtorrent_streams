import json

import requests
from rest_framework.exceptions import ValidationError
from sentry_sdk import capture_message

from backend import settings


def validate_captcha(token):
    try:
        r = requests.post(settings.RECAPTCHA_ENDPOINT, {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token
        })
        response_data = json.loads(r.content.decode())
        success = response_data['success']
        action = response_data["action"]
        score = response_data["score"]
    except Exception as e:
        capture_message(f"Captcha server unavailable, {e}", level="error")
        return

    if not (success and score > settings.RECAPTCHA_REQUIRED_SCORES.get(action, 2)):
        raise ValidationError(detail={"captcha": "bad captcha"})
