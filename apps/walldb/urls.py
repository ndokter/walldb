from django.conf.urls import patterns, url, include

from apps.walldb.views import user
from apps.walldb.views import wallpaper
from apps.walldb.views import walldb


user_patterns = patterns('',
    url(r'^(?P<id>\d+)/$', user.UserDetailView.as_view(), name='details'),
    url(r'^edit/$', user.UserEditView.as_view(), name='edit'),
    # url(r'^list/$', user.UserListView.as_view(), name='list'),
    url(r'^authentication/login/$', user.UserAuthenticationLoginView.as_view(), name='auth-login'),
    url(r'^authentication/logout/$', user.UserAuthenticationLogoutView.as_view(), name='auth-logout'),
    url(r'^authentication/register/$', user.UserAuthenticationRegisterView.as_view(), name='auth-register'),
)

wallpaper_patterns = patterns('',
    url(r'^list/$', wallpaper.WallpaperListView.as_view(), name='list'),
    url(r'^upload/$', wallpaper.WallpaperUploadView.as_view(), name='upload'),
    url(r'^(?P<hash>\w+)/$', wallpaper.WallpaperDetailView.as_view(), name='details'),
)

urlpatterns = patterns('',
    url(r'^$', walldb.IndexView.as_view(), name='index'),
    url(r'^changelog/$', walldb.ChangeLogView.as_view(), name='changelog'),

    url(r'wallpaper/', include(wallpaper_patterns, namespace='wallpaper')),
    url(r'user/', include(user_patterns, namespace='user')),
)
