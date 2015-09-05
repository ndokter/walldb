import re
import time
import random
import requests

from bs4 import BeautifulSoup

from apps.wallpaper.lib.wallpaper_scraper.base import Scraper


class RedditBaseScraper(Scraper):
    BASE_URL = None
    MAX_PAGES = 5
    _next_page_url = BASE_URL
    _scraped_pages = 0

    def get_urls(self, limit):
        urls = []

        while len(urls) < limit and self._scraped_pages < self.MAX_PAGES:
            urls += self._get_wallpaper_urls()

            time.sleep(random.randint(2, 5))

            self._scraped_pages += 1

        return urls

    def _get_wallpaper_urls(self):
        response = requests.get(
            self._next_page_url,
            headers={'User-Agent': self.USER_AGENT}
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        # The next page URL uses some random value that needs to be scraped.
        next_page_el = soup.find(name='a', rel='nofollow next')

        self._next_page_url = next_page_el['href']

        # Imgur wallpaper links
        link_els = soup.findAll(
            name='a',
            href=re.compile(
                r'http:\/\/i\.imgur\.com\/[A-Za-z0-9]{2,10}(\.jpg|\.png)'
            )
        )

        return list(set([link_el['href'] for link_el in link_els]))


class RedditWallpapersScraper(RedditBaseScraper):
    BASE_URL = 'http://www.reddit.com/r/wallpapers/new'
    _next_page_url = BASE_URL


class RedditWallpaperScraper(RedditBaseScraper):
    BASE_URL = 'http://www.reddit.com/r/wallpaper/new'
    _next_page_url = BASE_URL
