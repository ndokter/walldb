from io import BytesIO

import time
import random
import logging
import requests
import sys
import uuid

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

    def scrape(self, url):
        logger.info("Started downloading '%s'", url)

        response = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        file_type, extension = response.headers.get('content-type').split('/')

        downloaded_file = SimpleUploadedFile(
            name='w_{}.{}'.format(str(uuid.uuid4()), extension),
            content=response.content,
            content_type=response.headers.get('content-type')
        )

        form = WallpaperForm(files={'file': downloaded_file})

        if not form.is_valid():
            logger.info("Image '%s' did not validate: '%s'", url, form.errors)
            return

        wallpaper = form.save()

        logger.info("Saved image '%s' with hash '%s'", url, wallpaper.hash)

        thumb_file = SimpleUploadedFile(
            name='t_{}.{}'.format(str(uuid.uuid4()), wallpaper.extension),
            content=create_thumbnail(wallpaper.file, wallpaper.extension),
            content_type=response.headers.get('content-type')
        )

        Thumbnail(wallpaper=wallpaper, file=thumb_file).save()

        time.sleep(random.randint(1, 5))