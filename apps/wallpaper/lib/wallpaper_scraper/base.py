from abc import ABCMeta


class PageDoesNotExistError(Exception):
    pass


class Scraper(object):
    __metaclass__ = ABCMeta

    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'

    def get_urls(self, limit):
        """
        Returns an iterable containing hyperlinks to wallpapers. Limit indicates the
        maximum amount of returned links.
        """
        pass
