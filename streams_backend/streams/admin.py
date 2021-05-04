from django.contrib import admin

# Register your models here.
from streams.models import Chunk, Stream, Tracker


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    pass


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'stream_id', 'number', 'file_url', 'torrent_path']
    pass


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    pass
