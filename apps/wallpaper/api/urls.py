from django.conf.urls import patterns, url

from apps.wallpaper.api.views.wallpaper_detail import WallpaperDetailAPIView
from apps.wallpaper.api.views.wallpaper_favorite import WallpaperFavoriteAPIView
from apps.wallpaper.api.views.wallpaper_list import WallpaperListAPIView, \
    WallpaperFavoritedListAPIView, WallpaperRatedListAPIView
from apps.wallpaper.api.views.wallpaper_rating import WallpaperRatingAPIView


api_v1_patterns = patterns('',
    url(r'^favorites/list/$', WallpaperFavoritedListAPIView.as_view(), name='favorites-list'),
    url(r'^ratings/list/$', WallpaperRatedListAPIView.as_view(), name='ratings-list'),
    url(r'^list/$', WallpaperListAPIView.as_view(), name='list'),
    url(r'^(?P<hash>\w+)/favorite/$', WallpaperFavoriteAPIView.as_view(), name='favorite'),
    url(r'^(?P<hash>\w+)/rate/$', WallpaperRatingAPIView.as_view(), name='rate'),
    url(r'^(?P<hash>\w+)/$', WallpaperDetailAPIView.as_view(), name='detail'),
)
