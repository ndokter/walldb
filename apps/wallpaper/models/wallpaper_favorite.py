from django.contrib.auth.models import User
from django.db import models


class WallpaperFavorite(models.Model):
    wallpaper = models.ForeignKey('wallpaper.Wallpaper', related_name='favorites')
    user = models.ForeignKey(User, related_name='wallpaper_favorites', db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('wallpaper', 'user'),)
