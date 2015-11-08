from apps.wallpaper.lib.wallpaper_scraper.base import Scraper


class TestScraper(Scraper):
    """
    Dummy scraper for testing / developing.
    """
    def get_urls(self, limit):
        return (
            # 'http://walldb.net/media/images/w_5c0bd20fcbeca27b84e36a4be5af0443c3a756db.jpeg',
            'http://walldb.net/media/images/w_95d659129014e452d09420d2da8de3a99c2489a2.png',
        )
