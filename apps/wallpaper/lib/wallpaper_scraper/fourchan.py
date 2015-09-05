import random
import re
import time
import requests

from bs4 import BeautifulSoup

from apps.wallpaper.lib.wallpaper_scraper.base import Scraper, PageDoesNotExistError


class FourChanScraper(Scraper):
    BASE_URL = 'http://boards.4chan.org/wg/{page_number}'
    current_page = 2  # skip the less moderated first page
    MAX_PAGES = 10 - current_page  # 4Chan has 10 pages

    def get_urls(self, limit):
        """
        Fetch wallpaper urls by going through 4Chan's wallpaper pages. It keeps
        collecting till the limit is reached, or the maximum browsable pages has
        been reached.
        """
        urls = []

        while len(urls) < limit:
            try:
                page_url = self._next_page_url()
            except PageDoesNotExistError:
                break

            urls += self._get_wallpaper_urls(page_url)
            time.sleep(random.randint(1, 3))

        return urls[:limit]

    def _next_page_url(self):
        """
        4Chan is paginated. Get the url to the next (or first) page to get
        wallpaper urls from.
        """
        new_page = self.current_page + 1

        if new_page > FourChanScraper.MAX_PAGES:
            raise PageDoesNotExistError('Page: \'{}\' does not exist'.format(new_page))

        self.current_page = new_page

        return FourChanScraper.BASE_URL.format(page_number=self.current_page)

    def _get_wallpaper_urls(self, page_url):
        """
        Return all wallpaper links on the given page.
        """
        response = requests.get(page_url, headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(response.text)
        soup_els = soup.findAll(name='a', href=re.compile(r'./[0-9]{5,13}(.jpg|.png)'))

        # Format wallpaper to be a complete url with 'http://' prefixed.
        return list(set([self._format_wallpaper_url(el['href']) for el in soup_els]))

    def _format_wallpaper_url(self, url):
        return 'http://{}'.format(url.replace("//", ""))
