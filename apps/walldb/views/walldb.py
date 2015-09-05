from django.contrib.auth.models import User
from django.views.generic import TemplateView

from apps.wallpaper.models.wallpaper import Wallpaper


class IndexView(TemplateView):
    template_name = 'walldb/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(IndexView, self).get_context_data(**kwargs)

        context_data.update(
            statistics={
                'wallpaper_count': Wallpaper.objects.active().count(),
                'user_count': User.objects.filter(is_active=True).count()
            }
        )

        return context_data


class ChangeLogView(TemplateView):
    template_name = 'walldb/changelog.html'
