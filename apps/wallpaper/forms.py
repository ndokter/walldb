from PIL import Image as PILImage

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

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
        ('random', _('Random')),
        ('-created', _('Latest')),
        ('created', _('First')),
    )

    resolution = forms.ChoiceField(choices=RESOLUTION_CHOICES, required=True)
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=True)


class WallpaperForm(forms.ModelForm):
    MIN_PIXELS = 1280 * 960  # 1.3~ mega pixels
    MIN_IMAGE_PX_WIDTH = 400
    MAX_IMAGE_PX_WIDTH = 10000
    MIN_IMAGE_PX_HEIGHT = 400
    MAX_IMAGE_PX_HEIGHT = 10000

    def clean_file(self):
        """
        Validate the file on the following:
        - hash: dont allow duplicate images
        - width: sensible min and max image width
        - height: sensible min and max image height
        - megapixels: the combined width and height should yield a minimal size
        """
        # Check file hash.
        self.cleaned_data['file'].seek(0)
        image_hash = file_hash(self.cleaned_data['file'])

        if Wallpaper.objects.filter(hash=image_hash).exists():
            raise ValidationError(
                'Wallpaper with hash \'{}\' already exists'.format(image_hash)
            )

        # Check image width and height.
        self.cleaned_data['file'].file.seek(0)
        image_width, image_height = PILImage.open(self.cleaned_data['file'].file).size

        if WallpaperForm.MIN_IMAGE_PX_WIDTH < image_width > WallpaperForm.MAX_IMAGE_PX_WIDTH:
            raise ValidationError(
                "Wallpaper image width should be between '{}' and '{}' pixels".format(
                    WallpaperForm.MIN_IMAGE_PX_WIDTH,
                    WallpaperForm.MAX_IMAGE_PX_WIDTH
                )
            )

        if WallpaperForm.MIN_IMAGE_PX_HEIGHT < image_height > WallpaperForm.MAX_IMAGE_PX_HEIGHT:
            raise ValidationError(
                "Wallpaper image height should be between '{}' and '{}' pixels".format(
                    WallpaperForm.MIN_IMAGE_PX_HEIGHT,
                    WallpaperForm.MAX_IMAGE_PX_HEIGHT
                )
            )

        # Validate a wallpaper to have a minimum amount of mega pixels
        if (image_width * image_height) < WallpaperForm.MIN_PIXELS:
            raise ValidationError(
                'Image size of \'{}x{}\' does not meet the minimum requirement'
                'of at least 1.3 mega pixels (about \'1280x960\' for example).'
                .format(image_width, image_height)
            )

        return self.cleaned_data['file']

    class Meta:
        fields = ('file',)
        model = Wallpaper


class WallpaperRatingForm(forms.ModelForm):

    class Meta:
        model = WallpaperRating
        fields = ('score',)
