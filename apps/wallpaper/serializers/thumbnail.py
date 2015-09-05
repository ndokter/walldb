from rest_framework import serializers

from apps.wallpaper.models.thumbnail import Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ('file',)
