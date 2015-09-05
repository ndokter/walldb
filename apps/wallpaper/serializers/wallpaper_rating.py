from rest_framework import serializers

from apps.wallpaper.models.wallpaper_rating import WallpaperRating


class WallpaperRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallpaperRating
