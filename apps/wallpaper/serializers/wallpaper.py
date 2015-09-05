from rest_framework import serializers

from apps.wallpaper.models.wallpaper import Wallpaper
from apps.wallpaper.serializers.thumbnail import ThumbnailSerializer


class WallpaperSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True)
    user_rating = serializers.IntegerField()
    user_favorite = serializers.BooleanField()

    class Meta:
        model = Wallpaper
        fields = ('pk', 'width', 'height', 'created', 'hash', 'file', 'title',
                  'thumbnails', 'user_rating', 'user_favorite',)
