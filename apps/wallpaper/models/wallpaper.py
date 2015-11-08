import datetime
from django.db import models

from apps.wallpaper.mixins.model import SeededRandomQuerySetMixin
from apps.wallpaper.models.image import Image


class WallpaperQuerySet(SeededRandomQuerySetMixin, models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def include_user_ratings(self, user):
        return self.extra(
            select={
                'user_rating': """
                    SELECT score
                    FROM wallpaper_wallpaperrating r
                    WHERE wallpaper_wallpaper.image_ptr_id = r.wallpaper_id
                    AND r.user_id = %s
                """
            },
            select_params=[getattr(user, 'pk', None)]
        )

    def include_user_favorites(self, user):
        return self.extra(
            select={
                'user_favorite': """
                    SELECT 1
                    FROM wallpaper_wallpaperfavorite f
                    WHERE wallpaper_wallpaper.image_ptr_id = f.wallpaper_id
                    AND f.user_id = %s
                """
            },
            select_params=[getattr(user, 'pk', None)]
        )


class Wallpaper(Image):
    objects = WallpaperQuerySet.as_manager()

    active = models.NullBooleanField(db_index=True, default=None)
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)

    def accept(self):
        self.active = True
        self.created = datetime.datetime.now()  # for proper list ordering

        self.save()

    def reject(self):
        """
        Reject the wallpaper by making it inactive and removing the wallpaper
        file to save space. Keep the thumbnails for easier recognition.
        """
        self.active = False

        # TODO maybe do this some day if extra space is needed.
        #self.file.delete(False)

        self.save()
