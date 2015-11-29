import logging

from django.core.management.base import BaseCommand
from PIL import Image as PILImage

from apps.wallpaper.models import Wallpaper

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        wallpaper = Wallpaper.objects.get(hash='247ffde52a913a7ca22e63b9136504334655e43a')

        img = PILImage.open(wallpaper.file)
        img = img.convert('RGB')

        colors = {}

        for color in img.getdata():
            colors[color] = colors.get(color, 0) + 1

        print colors


