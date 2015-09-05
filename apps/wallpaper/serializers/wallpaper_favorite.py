from rest_framework import serializers

from apps.wallpaper.models.wallpaper_favorite import WallpaperFavorite


class WallpaperFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallpaperFavorite
