from django.contrib.auth.models import User
from django.db import models


class WallpaperRating(models.Model):
    """
    Wallpaper rating score. Currently only supports 1 or -1, but could be
    transformed to a 5 star rating system in the future.
    """
    RATING_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike')
    )

    wallpaper = models.ForeignKey('wallpaper.Wallpaper', related_name='ratings')
    user = models.ForeignKey(User, related_name='wallpaper_ratings', db_index=True)

    score = models.IntegerField(choices=RATING_CHOICES)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('wallpaper', 'user'),)
