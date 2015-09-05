from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from apps.wallpaper.api.urls import api_v1_patterns as wallpaper_api_v1_patterns


api_v1_patterns = patterns('',
    url(r'wallpaper/', include(wallpaper_api_v1_patterns, namespace='wallpaper')),
)

api_version_patterns = patterns('',
    url(r'v1/', include(api_v1_patterns, namespace='v1')),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_version_patterns, namespace='api')),
    url(r'', include('apps.walldb.urls', namespace='walldb')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
