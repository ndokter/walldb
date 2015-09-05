from django.shortcuts import get_object_or_404

from apps.wallpaper.models.wallpaper import Wallpaper


class WallpaperMixin(object):
    wallpaper = None

    def dispatch(self, *args, **kwargs):
        self.wallpaper = get_object_or_404(Wallpaper, hash=kwargs.get('hash'))

        return super(WallpaperMixin, self).dispatch(*args, **kwargs)
