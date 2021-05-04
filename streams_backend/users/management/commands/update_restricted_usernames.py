from django.core.management.base import BaseCommand

from users.models import User

RESTRICTED_USERNAMES = [
    "settings",
    "account",
]


class Command(BaseCommand):
    help = 'Create users with restricted username'

    def handle(self, *args, **options):
        for username in RESTRICTED_USERNAMES:
            User.objects.filter(username__in=RESTRICTED_USERNAMES).update(username=f"{username}1")
