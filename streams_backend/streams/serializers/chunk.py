from rest_framework import serializers

from streams.models import Chunk


class ChunkSerializer(serializers.ModelSerializer):
    torrent_url = serializers.SerializerMethodField()

    class Meta:
        model = Chunk
        fields = ["number", "duration", "torrent_url", "magnet_link", "prob", ]

    def get_torrent_url(self, obj: Chunk):
        return obj.torrent_url if obj.prob else None
