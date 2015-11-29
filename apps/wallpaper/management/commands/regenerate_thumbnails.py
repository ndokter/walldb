import uuid
import logging

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from apps.wallpaper.helpers.image import create_thumbnail
from apps.wallpaper.models import Wallpaper
from apps.wallpaper.models.thumbnail import Thumbnail


logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Regenerate thumbnails.'

    def handle(self, *args, **options):
        wallpapers = Wallpaper.objects.all()
        wallpaper_count = wallpapers.count()

        logger.info(
            'Regenerating thumbnails for %s wallpapers',
            wallpaper_count
        )

        for i, wallpaper in enumerate(wallpapers):
            logger.info(
                '#%s/%s regenerating thumbnail for wallpaper %s',
                i,
                wallpaper_count,
                wallpaper
            )

            self._regenerate_thumbnails(wallpaper)

    def _regenerate_thumbnails(self, wallpaper):

        wallpaper.thumbnails.all().delete()

        thumbnail_file = create_thumbnail(
            image_file=wallpaper.file,
            file_extension=wallpaper.extension
        )

        thumb_file = SimpleUploadedFile(
            name='t_{}.{}'.format(str(uuid.uuid4()), wallpaper.extension),
            content=thumbnail_file,
        )

        Thumbnail(wallpaper=wallpaper, file=thumb_file).save()

        thumb_file.close()