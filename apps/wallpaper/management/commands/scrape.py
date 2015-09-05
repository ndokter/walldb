from io import BytesIO

import time
import random
import logging
import requests
import sys

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from PIL import Image

from apps.wallpaper.forms import WallpaperForm
from apps.wallpaper.helpers.file import file_hash
from apps.wallpaper.helpers.image import create_thumbnail
from apps.wallpaper.lib.wallpaper_scraper.fourchan import FourChanScraper
from apps.wallpaper.lib.wallpaper_scraper.reddit import RedditWallpaperScraper, \
    RedditWallpapersScraper
from apps.wallpaper.lib.wallpaper_scraper.test import TestScraper
from apps.wallpaper.models.thumbnail import Thumbnail


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape wallpapers using the selected client.'
    args = '<client> <limit>'

    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
    CLIENTS = {
        '4chan': FourChanScraper,
        'reddit__wallpaper': RedditWallpaperScraper,
        'reddit__wallpapers': RedditWallpapersScraper,
        'test': TestScraper
    }

    def handle(self, *args, **options):
        try:
            client_name, limit = args[0], int(args[1])
        except (IndexError, ValueError):
            raise CommandError('Required parameters are: {}'.format(self.args))

        try:
            client_class = self.CLIENTS[client_name]
        except KeyError:
            raise CommandError(
                'Client: \'{}\' does not exist. Supported options: \'{}\''.format(
                    client_name,
                    self.CLIENTS.keys()
                )
            )

        client = client_class()
        urls = client.get_urls(limit)

        logger.info(
            "Client '%s' scraped '%s' links to download.",
            client_name,
            len(urls)
        )

        for url in urls:
            self.scrape(url)

    # TODO make logic more reusable.
    def scrape(self, url):
        logger.info("Started downloading '%s'", url)

        response = requests.get(url, headers={'User-Agent': self.USER_AGENT})

        file_type, extension = response.headers.get('content-type').split('/')

        form = WallpaperForm(files={'file': SimpleUploadedFile(
            name='tmp.{extension}'.format(extension=extension),
            content=response.content,
            content_type=response.headers.get('content-type')
        )})

        if not form.is_valid():
            logger.info("Image '%s' did not validate: '%s'", url, form.errors)

            return

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

        logger.info("Saved image '%s' with hash '%s'", url, wallpaper.hash)

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

        time.sleep(random.randint(1, 5))
