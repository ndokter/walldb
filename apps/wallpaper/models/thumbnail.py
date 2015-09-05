from django.db import models

from apps.wallpaper.models.image import Image


class Thumbnail(Image):
    wallpaper = models.ForeignKey('wallpaper.Wallpaper', related_name='thumbnails')
