from io import BytesIO

import os
import sys
import logging

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from apps.wallpaper.forms import WallpaperForm
from apps.wallpaper.helpers.file import file_hash
from apps.wallpaper.helpers.image import create_thumbnail
from apps.wallpaper.models.thumbnail import Thumbnail


logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Import files from folder.'
    args = '<folder>'

    def handle(self, *args, **options):
        folder_path = args[0]

        for file_name in os.listdir(folder_path):
            self.import_file(folder_path, file_name)

    # TODO make logic more reusable.
    def import_file(self, folder_path, file_name):
        full_path = folder_path + file_name
        extension = file_name.split('.')[-1]
        f = open(full_path, "rb")

        if extension == 'jpg':
            extension = 'jpeg'

        form = WallpaperForm(files={'file': SimpleUploadedFile(
            name='tmp.{extension}'.format(extension=extension),
            content=f.read(),
            content_type=extension
        )})

        if form.is_valid():
            logger.info('Saving image \'{}\''.format(file_name))

            # Wallpaper
            wallpaper = form.save(commit=False)
            wallpaper.size = form.cleaned_data['file'].size
            wallpaper.hash = file_hash(form.cleaned_data['file'])
            form.cleaned_data['file'].file.seek(0)
            wallpaper.width, wallpaper.height = Image.open(form.cleaned_data['file'].file).size
            wallpaper.extension = extension

            wallpaper.file.save(
                'w_{hash}.{extension}'.format(hash=wallpaper.hash, extension=wallpaper.extension),
                form.cleaned_data['file']
            )

            wallpaper.save()

            # Thumbnail
            form.cleaned_data['file'].file.seek(0)

            thumb_file = create_thumbnail(form.cleaned_data['file'].file, extension)
            thumb_width, thumb_height = Image.open(BytesIO(thumb_file)).size

            thumbnail = Thumbnail(
                size=sys.getsizeof(thumb_file),
                wallpaper=wallpaper,
                hash=file_hash(BytesIO(thumb_file)),
                width=thumb_width,
                height=thumb_height,
                extension=extension
            )

            thumbnail.file.save(
                't_{hash}.{extension}'.format(hash=thumbnail.hash, extension=extension),
                ContentFile(thumb_file)
            )

            thumbnail.save()
        else:
            logger.info('Image \'{}\' did not validate: \'{}\''.format(file_name, form.errors))

        os.remove(full_path)
