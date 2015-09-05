from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from apps.wallpaper.mixins.view import WallpaperMixin
from apps.wallpaper.serializers.wallpaper_rating import WallpaperRatingSerializer


class WallpaperRatingAPIView(WallpaperMixin, APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WallpaperRatingSerializer

    def get_serializer_data(self):
        return {
            'wallpaper': self.wallpaper.pk,
            'user': self.request.user.pk,
            'score': self.request.data['score']
        }

    def put(self, request, *args, **kwargs):
        favorite = self.request.user.wallpaper_ratings.get(wallpaper=self.wallpaper)

        # The serializer gets it data partially the URL and Session, because the
        # user needs to be logged in to perform this action, and the the REST
        # like URL already contains the target (Wallpaper to rate).
        serializer = self.serializer_class(
            favorite,
            data=self.get_serializer_data(),
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        # The serializer gets it data partially the URL and Session, because the
        # user needs to be logged in to perform this action, and the the REST
        # like URL already contains the target (Wallpaper to rate).
        serializer = self.serializer_class(data=self.get_serializer_data())

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        self.request.user.wallpaper_ratings.get(wallpaper=self.wallpaper).delete()

        return Response(status=HTTP_204_NO_CONTENT)
