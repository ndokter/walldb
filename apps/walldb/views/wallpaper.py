import uuid
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from django.views.generic import DetailView, TemplateView
from django.forms.formsets import formset_factory

from apps.user.mixins import LoginRequiredMixin
from apps.wallpaper.forms import ImageFilterForm, WallpaperForm
from apps.wallpaper.helpers.image import create_thumbnail
from apps.wallpaper.mixins.view import WallpaperMixin
from apps.wallpaper.models.thumbnail import Thumbnail
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


class WallpaperUploadView(LoginRequiredMixin, TemplateView):
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

        if not formset.is_valid():
            context = self.get_context_data(**kwargs)
            context['formset'] = formset

            return self.render_to_response(context)

        for form in formset:

            if not form.cleaned_data.get('file'):
                continue

            uploaded_file = form.cleaned_data['file']
            file_type, extension = uploaded_file.content_type.split('/')

            wallpaper = form.save(commit=False)
            wallpaper.uploaded_by = request.user
            wallpaper.file.name = 'w_{}.{}'.format(str(uuid.uuid4()), extension)
            wallpaper.save()

            thumb_file = SimpleUploadedFile(
                name='t_{}.{}'.format(str(uuid.uuid4()), wallpaper.extension),
                content=create_thumbnail(wallpaper.file, wallpaper.extension),
                content_type=uploaded_file.content_type
            )

            Thumbnail(wallpaper=wallpaper, file=thumb_file).save()

        messages.add_message(
            request,
            messages.SUCCESS,
            "Your wallpapers have succesfully been uploaded. They will get " +
            "visible under 'uploaded' and to other users after they have been" +
            " accepted."
        )

        return redirect(
            reverse_lazy('walldb:user:details', kwargs={'id': request.user.pk})
        )
