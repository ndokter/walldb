from django.views.generic import DetailView, TemplateView
from django.forms.formsets import formset_factory

from apps.wallpaper.forms import ImageFilterForm, WallpaperForm
from apps.wallpaper.mixins.view import WallpaperMixin
from apps.wallpaper.models.wallpaper import Wallpaper


class WallpaperListView(TemplateView):
    template_name = 'walldb/wallpaper/list.html'
    form_class = ImageFilterForm

    def get_context_data(self, **kwargs):
        context_data = super(WallpaperListView, self).get_context_data(**kwargs)
        context_data['filter_form'] = ImageFilterForm(self.request.GET or None)

        return context_data


class WallpaperDetailView(WallpaperMixin, DetailView):
    template_name = 'walldb/wallpaper/detail.html'
    model = Wallpaper

    def get_object(self, queryset=None):
        return self.wallpaper


class WallpaperUploadView(TemplateView):
    template_name = 'walldb/wallpaper/upload.html'

    WallpaperFormSet = formset_factory(WallpaperForm,
                                       min_num=1,
                                       max_num=5,
                                       extra=4,
                                       validate_min=True)

    def get_context_data(self, **kwargs):
        context_data = super(WallpaperUploadView, self)\
            .get_context_data(**kwargs)

        context_data['formset'] = self.WallpaperFormSet()

        return context_data

    def post(self, request, *args, **kwargs):
        formset = self.WallpaperFormSet(request.POST, request.FILES)

        if formset.is_valid():
            # TODO work in progress
            pass

        return super(WallpaperUploadView, self).get(request, *args, **kwargs)
