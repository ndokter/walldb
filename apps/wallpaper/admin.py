import datetime

from django.contrib import admin

from apps.wallpaper.models.wallpaper import Wallpaper


def accept(modeladmin, request, queryset):
    for wallpaper in queryset:
        wallpaper.accept()


def reject(modelsadmin, request, queryset):
    for wallpaper in queryset:
        wallpaper.reject()


class WallpaperAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('dimensions', 'image_field', 'uploaded_by', 'active')
    actions = [accept, reject]

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
