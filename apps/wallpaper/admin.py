import datetime

from django.contrib import admin

from apps.wallpaper.models.wallpaper import Wallpaper


def make_active(modeladmin, request, queryset):
    # Update the created date to improve the 'latest' ordering.
    queryset.update(active=True,
                    created=datetime.datetime.now())


class WallpaperAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('dimensions', 'image_field', 'uploaded_by', 'active')
    actions = [make_active]

    def dimensions(self, obj):
        return '{object.width}x{object.height}'.format(object=obj)

    def image_field(self, obj):
        thumbnail_html = ''.join(
            ['<img src="{}" />'.format(thumbnail.file.url) for thumbnail in obj.thumbnails.all()]
        )

        return '<a href="{wallpaper_url}" target="_blank">{thumbnail_html}</a>'.format(
            wallpaper_url=obj.file.url,
            thumbnail_html=thumbnail_html
        )

    image_field.allow_tags = True


admin.site.register(Wallpaper, WallpaperAdmin)
