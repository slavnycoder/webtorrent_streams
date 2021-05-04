from django.core.management.base import BaseCommand

from streams.models import Stream
from users.models import User


class Command(BaseCommand):
    help = 'Create test stream'

    def handle(self, *args, **options):
        user = User.objects.get(username="django")
        stream, _ = Stream.objects.update_or_create(
            user=user,
            description="The Legend of Zelda: Breath of the Wild",
            viewers=7596,
        )
        user.stream = stream
        user.save()
