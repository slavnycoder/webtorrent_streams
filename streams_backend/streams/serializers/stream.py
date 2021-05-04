from rest_framework import serializers

from streams.models import Stream


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ("id", "description", "is_live", "viewers", "thumbnail_url", "playlist_json_url")
