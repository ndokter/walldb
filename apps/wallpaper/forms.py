from PIL import Image as PILImage

from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from io import BytesIO

from apps.wallpaper.helpers.file import file_hash
from apps.wallpaper.models.wallpaper import Wallpaper
from apps.wallpaper.models.wallpaper_rating import WallpaperRating


class ImageFilterForm(forms.Form):
    """
    Used for filtering displayed images.
    """
    RESOLUTION_CHOICES = (
        ('', 'All resolutions'),
        ('1280x960', '1280x960'),
        ('1280x1024', '1280x1024'),
        ('1366x768', '1366x960'),
        ('1440x900', '1440x900'),
        ('1400x1050', '1400x1050'),
        ('1600x900', '1600x900'),
        ('1600x1200', '1600x1200'),
        ('1680x1050', '1680x1050'),
        ('1920x1080', '1920x1080'),
        ('1920x1200', '1920x1200'),
        ('2048x2048', '2048x2048 (ipad)'),
        ('2560x1440', '2560x1440'),
        ('2560x1600', '2560x1600'),
        ('2560x2048', '2560x2048'),
    )
    ORDERING_CHOICES = (
        ('random', 'Random'),
        ('-created', 'Latest'),
        ('created', 'First'),
    )

    resolution = forms.ChoiceField(choices=RESOLUTION_CHOICES, required=True)
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=True)


class WallpaperForm(forms.ModelForm):
    MIN_PIXELS = 1280 * 960  # 1.3~ mega pixels
    MIN_IMAGE_PX_WIDTH = 400
    MAX_IMAGE_PX_WIDTH = 10000
    MIN_IMAGE_PX_HEIGHT = 400
    MAX_IMAGE_PX_HEIGHT = 10000

    MAX_FILE_SIZE = 10240  # in KB's

    file = forms.ImageField(
        widget=forms.FileInput(attrs={'data-max-file-size': MAX_FILE_SIZE})
    )

    def clean_file(self):
        """
        Validate the file on the following:
        - file type: only allow .jpeg and .png
        - file size: check the maximum file size
        - hash: dont allow duplicate images
        - width: sensible min and max image width
        - height: sensible min and max image height
        - megapixels: the combined width and height should yield a minimal size
        """
        file_name = self.cleaned_data['file'].name

        # Check file type.
        # We need to get a file object for PIL. We might have a path or we
        # might have to read the data into memory.
        if hasattr(self.cleaned_data['file'], 'temporary_file_path'):
            f = self.cleaned_data['file'].temporary_file_path()
        elif hasattr(self.cleaned_data['file'], 'read'):
            f = BytesIO(self.cleaned_data['file'].read())
        else:
            f = BytesIO(self.cleaned_data['file']['content'])

        try:
            img = PILImage.open(f)
        except Exception:
            # Python Imaging Library doesn't recognize it as an image
            raise ValidationError(
                'Unsupported image type. Please upload png or jpeg. ({})'.format(
                    file_name
                )
            )

        if img.format not in ('PNG', 'JPEG'):
            raise ValidationError(
                'Unsupported image type. Please upload png or jpeg ({})'.format(
                    file_name
                )
            )

        # Check file size
        if self.cleaned_data['file'] \
                and self.cleaned_data['file']._size > self.MAX_FILE_SIZE * 1024:
            raise ValidationError(
                'Please limit the file size to under {}MB ({})'.format(
                    self.MAX_FILE_SIZE / 1024,
                    file_name
                )
            )

        # Check file hash.
        self.cleaned_data['file'].seek(0)
        image_hash = file_hash(self.cleaned_data['file'])

        try:
            wallpaper = Wallpaper.objects.get(hash=image_hash)
        except Wallpaper.DoesNotExist:
            pass
        else:
            error_msg = 'This wallpaper already exists'

            if wallpaper.active is True:
                error_msg += ' (<a href="{}" target="_blank">{}</a>)'.format(
                    reverse('walldb:wallpaper:details', args=(image_hash,)),
                    image_hash
                )
            elif wallpaper.active is None:
                error_msg += ', but has not yet been accepted'
            elif wallpaper.active is False:
                error_msg += ', but was rejected based on quality or content'

            error_msg += ' ({})'.format(file_name)

            raise ValidationError(mark_safe(error_msg))

        # Check image width and height.
        self.cleaned_data['file'].file.seek(0)
        image_width, image_height = PILImage.open(self.cleaned_data['file'].file).size

        if WallpaperForm.MIN_IMAGE_PX_WIDTH < image_width > WallpaperForm.MAX_IMAGE_PX_WIDTH:
            raise ValidationError(
                "Wallpaper image width should be between '{}' and '{}' pixels"
                " ({})"
                .format(
                    WallpaperForm.MIN_IMAGE_PX_WIDTH,
                    WallpaperForm.MAX_IMAGE_PX_WIDTH,
                    file_name
                )
            )

        if WallpaperForm.MIN_IMAGE_PX_HEIGHT < image_height > WallpaperForm.MAX_IMAGE_PX_HEIGHT:
            raise ValidationError(
                "Wallpaper image height should be between '{}' and '{}' pixels"
                " ({})"
                .format(
                    WallpaperForm.MIN_IMAGE_PX_HEIGHT,
                    WallpaperForm.MAX_IMAGE_PX_HEIGHT,
                    file_name
                )
            )

        # Validate a wallpaper to have a minimum amount of mega pixels
        if (image_width * image_height) < WallpaperForm.MIN_PIXELS:
            raise ValidationError(
                'Image size of \'{}x{}\' does not meet the minimum requirement'
                ' of at least 1.3 mega pixels (about \'1280x960\' for example)'
                ' ({})'
                .format(
                    image_width,
                    image_height,
                    file_name
                )
            )

        return self.cleaned_data['file']

    class Meta:
        fields = ('file',)
        model = Wallpaper


class WallpaperRatingForm(forms.ModelForm):

    class Meta:
        model = WallpaperRating
        fields = ('score',)
