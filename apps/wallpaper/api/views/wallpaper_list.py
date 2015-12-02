from rest_framework import filters
from rest_framework.generics import ListAPIView

from apps.wallpaper.filters import RandomOrderingFilter, \
    WallpaperFavoritedFilter, WallpaperRatedFilter, WallpaperUploadedFilter
from apps.wallpaper.models.wallpaper import Wallpaper
from apps.wallpaper.serializers.wallpaper import WallpaperSerializer


class WallpaperListAPIView(ListAPIView):
    serializer_class = WallpaperSerializer
    filter_backends = (filters.DjangoFilterBackend, RandomOrderingFilter)
    filter_fields = ('width', 'height')
    ordering_fields = ('created',)
    ordering = ('?',)

    def get_queryset(self):
        return Wallpaper.objects\
            .active()\
            .include_user_ratings(self.request.user)\
            .include_user_favorites(self.request.user)\
            .prefetch_related('thumbnails')


class WallpaperFavoritedListAPIView(WallpaperListAPIView):
    filter_class = WallpaperFavoritedFilter
    ordering_fields = ('favorites__modified',)
    ordering = ('-favorites__modified',)

    def get_queryset(self):
        queryset = super(WallpaperFavoritedListAPIView, self).get_queryset()

        # Its important to use an exclude here because of filter chaining from
        # the filter set which causes double results
        # https://docs.djangoproject.com/en/1.8/topics/db/queries/#spanning-multi-valued-relationships
        return queryset.exclude(favorites__user__walldb_profile__is_public=False)


class WallpaperRatedListAPIView(WallpaperListAPIView):
    filter_class = WallpaperRatedFilter
    ordering_fields = ('ratings__modified',)
    ordering = ('-ratings__modified',)

    def get_queryset(self):
        queryset = super(WallpaperRatedListAPIView, self).get_queryset()

        # Its important to use an exclude here because of filter chaining from
        # the filter set which causes double results
        # https://docs.djangoproject.com/en/1.8/topics/db/queries/#spanning-multi-valued-relationships
        return queryset\
            .exclude(ratings__user__walldb_profile__is_public=False)\
            .exclude(ratings__score__lte=0)  # intended chaining for correct query


class WallpaperUploadedListAPIView(WallpaperListAPIView):
    filter_class = WallpaperUploadedFilter
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(WallpaperUploadedListAPIView, self).get_queryset()

        # Its important to use an exclude here because of filter chaining from
        # the filter set which causes double results
        # https://docs.djangoproject.com/en/1.8/topics/db/queries/#spanning-multi-valued-relationships
        return queryset\
            .exclude(uploaded_by__isnull=True,
                     uploaded_by__walldb_profile__is_public=False)
