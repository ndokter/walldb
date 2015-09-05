from apps.wallpaper.lib.wallpaper_scraper.base import Scraper


class TestScraper(Scraper):
    """
    Dummy scraper for testing / developing.
    """
    def get_urls(self, limit):
        return (
            'http://walldb.net/static/wallpapers/11e3bcf3cc796157f5d1f737880749.jpg',
            # 'http://i891.photobucket.com/albums/ac111/alicep69/MaterialeGrafico/Ornamenti%20vari%20in%20png/nievesitaa.png',
        )
