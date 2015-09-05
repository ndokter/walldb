from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from apps.wallpaper.mixins.view import WallpaperMixin
from apps.wallpaper.serializers.wallpaper_favorite import WallpaperFavoriteSerializer


class WallpaperFavoriteAPIView(WallpaperMixin, APIView):
    """
    Favorite wallpaper for the authenticated user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WallpaperFavoriteSerializer

    def post(self, request, *args, **kwargs):
        # The serializer gets it data from both the URL and Session, not the
        # post data. This is because the user needs to be logged in to perform
        # this action, and the the REST like URL already contains the target
        # (Wallpaper to favorite).
        serializer = self.serializer_class(data={
            'wallpaper': self.wallpaper.pk,
            'user': self.request.user.pk
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.wallpaper.favorites.get(user=self.request.user)
        instance.delete()

        return Response(status=HTTP_204_NO_CONTENT)