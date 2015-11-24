from rest_framework import filters

import django_filters

from apps.wallpaper.models import Wallpaper


class RandomOrderingFilter(filters.OrderingFilter):

    def get_ordering(self, request, queryset, view):
        if request.query_params.get(self.ordering_param) == 'random':
            return ('?',)

        return super(RandomOrderingFilter, self).get_ordering(
            request, queryset, view
        )

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if '?' in ordering and hasattr(type(queryset), 'seeded_random'):
            return queryset.seeded_random(
                float(request.query_params.get('seed', 0.0))
            )

        elif ordering:
            return queryset.order_by(*ordering)

        return queryset


class WallpaperFavoritedFilter(django_filters.FilterSet):

    user = django_filters.CharFilter(name='favorites__user__id')

    class Meta:
        model = Wallpaper
        fields = ('user',)


class WallpaperRatedFilter(django_filters.FilterSet):

    user = django_filters.CharFilter(name='ratings__user__id')

    class Meta:
        model = Wallpaper
        fields = ('user',)


class WallpaperUploadedFilter(django_filters.FilterSet):

    user = django_filters.CharFilter(name='uploaded_by')

    class Meta:
        model = Wallpaper
        fields = ('user',)
