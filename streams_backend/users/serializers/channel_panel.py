from rest_framework import serializers

from users.models import ChannelPanel


class ChannelPanelSerializer(serializers.ModelSerializer):
    image_src = serializers.SerializerMethodField()

    class Meta:
        model = ChannelPanel
        fields = ("id", "channel", "sort", "title", "image_src", "image_link", "text",)
        write_only_fields = ("channel",)

    def get_image_src(self, obj: ChannelPanel):
        return obj.image.file_url if obj.image else None
