from rest_framework.generics import RetrieveAPIView

from apps.wallpaper.models.wallpaper import Wallpaper
from apps.wallpaper.serializers.wallpaper import WallpaperSerializer


class WallpaperDetailAPIView(RetrieveAPIView):
    serializer_class = WallpaperSerializer
    lookup_field = 'hash'

    def get_queryset(self):
        return Wallpaper.objects\
            .active()\
            .include_user_ratings(self.request.user)\
            .include_user_favorites(self.request.user)
