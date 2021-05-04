from django.core.management.base import BaseCommand

from streams.models import Stream


class Command(BaseCommand):
    help = 'Delete offline streams'

    def handle(self, *args, **options):
        streams = Stream.objects.filter(is_live=False)
        for stream in streams:
            stream.delete()
