"""Module for all spiders."""


import os

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


CRAWL_DIR = get_project_settings()['DATA_DIR'] / 'crawl'


def extract_text(resp, min_tokens=3):
    """Extract all text from a web page.

    Args:
        resp (scrapy.Response): Response from HTTP request.
        min_tokens (int): Minimum number of tokens that must occur in page.

    Returns:
        List of strings with individual text elements found from the page.
    """
    selector = '//body/descendant-or-self::*[not(self::script)]/text()'
    texts = resp.selector.xpath(selector).extract()
    ret = []
    for text in texts:
        css_count = (text.count(';') + text.count(':') + text.count('#')
                     + text.count('{') + text.count('}'))
        if ((len(text) > 0)
            and (len(text.split()) >= min_tokens)
            and (css_count < 4)): # Avoid css styling as text
            ret.append(text.strip())
    return ret


class BaseSpider(Spider):
    """Base class spider for text extraction from a web page."""
    deny = ()
    allow = ()
    deny_domains = ()
    allowed_domains = ()

    def parse(self, resp):
        yield {
            'url': resp.url,
            'content': extract_text(resp)
        }
        for link in (LinkExtractor(allow_domains=self.allowed_domains,
                                   deny_domains=self.deny_domains,
                                   allow=self.allow,
                                   deny=self.deny)
                     .extract_links(resp)):
            yield Request(link.url, callback=self.parse)


class IltaLehtiSpider(BaseSpider):
    name = 'iltalehti'
    start_urls = ['https://www.iltalehti.fi']
    allowed_domains = ['iltalehti.fi']
    deny = (
        '.*replytocom\=.*'
    )
    custom_settings = {'JOBDIR': CRAWL_DIR / name}


class IltaSanomatSpider(BaseSpider):
    name = 'iltasanomat'
    start_urls = ['https://www.is.fi']
    allowed_domains = ['is.fi']
    custom_settings = {'JOBDIR': CRAWL_DIR / name}
    deny_domains = (
        'ravit.is.fi'
    )
    deny = (
        '.*/tag/.*',
        '.*/haku/.*'
    )


class Yle(BaseSpider):
    name = 'yle'
    start_urls = ['https://www.yle.fi']
    allowed_domains = ['yle.fi']
    custom_settings = {'JOBDIR': CRAWL_DIR / name}
    deny_domains = (
        'atuubi.yle.fi',
        'arenan.yle.fi',
        'svenska.yle.fi'
    )
    deny = (
        '.*autoplay\='
    )


class MTVUutiset(BaseSpider):
    name = 'mtvuutiset'
    start_urls = ['https://www.mtvuutiset.fi']
    allowed_domains = ['mtvuutiset.fi']
    custom_settings = {'JOBDIR': CRAWL_DIR / name}


class Suomi24(BaseSpider):
    name = 'suomi24'
    start_urls = ['https://keskustelu.suomi24.fi']
    allowed_domains = ['keskustelu.suomi24.fi']
    custom_settings = {'JOBDIR': CRAWL_DIR / name}


class Ylilauta(BaseSpider): # NOT WORKING!
    name = 'ylilauta'
    start_urls = ['https://ylilauta.org']
    allowed_domains = ['ylilauta.org']
    custom_settings = {'JOBDIR': CRAWL_DIR / name}


class Vauva(BaseSpider):
    name = 'vauva'
    start_urls = ['https://www.vauva.fi/keskustelu']
    allowed_domains = ['vauva.fi']
    custom_settings = {'JOBDIR': CRAWL_DIR / name}
    allow = ('.*/keskustelu/.*')
    deny = (
        '.*rate\=.*',
        '.*quote\=.*'
    )


class Demi(BaseSpider):
    name = 'demi'
    start_urls = ['https://www.demi.fi/keskustelut']
    allowed_domains = ['demi.fi']
    allow = (
        '.*/keskustelut/.*'
    )
    custom_settings = {'JOBDIR': CRAWL_DIR / name}


class Tori(BaseSpider):
    name = 'tori'
    start_urls = ['https://www.tori.fi']
    allowed_domains = ['tori.fi']
    allow = (
    )
    custom_settings = {'JOBDIR': CRAWL_DIR / name}

class Kauppalehti(BaseSpider):  # NOT WORKING!
    name = 'kauppalehti'
    start_urls = ['https://www.kauppalehti.fi']
    allowed_domains = ['kauppalehti.fi']
    allow = (
    )
    custom_settings = {'JOBDIR': CRAWL_DIR / name}

class Kotikokki(BaseSpider):
    name = 'kotikokki'
    start_urls = ['https://www.kotikokki.net']
    allowed_domains = ['kotikokki.net']
    allow = (
    )
    deny = (
        '.*//.*'
    )
    custom_settings = {'JOBDIR': CRAWL_DIR / name}

class Oikotie(BaseSpider): # NOT WORKING!
    name = 'oikotie'
    start_urls = ['https://www.oikotie.fi']
    allowed_domains = ['oikotie.fi']
    allow = (
    )
    custom_settings = {'JOBDIR': CRAWL_DIR / name}