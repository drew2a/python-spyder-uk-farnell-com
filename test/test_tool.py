import glob
import os
import unittest

from scrapy import Request
from scrapy.http import HtmlResponse

from spyder_uk_farnell_com.spiders.uk_farnell_com_spider import UkSpider


class TestSpider(unittest.TestCase):
    def setUp(self):
        self.pages = {}
        self.pages_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_pages')

        html_files = glob.glob(os.path.join(
            self.pages_folder,
            '*.html'))

        for filename in html_files:
            key = os.path.basename(filename)
            with open(filename, encoding="utf8") as file:
                self.pages[key] = file.read()

    def parse_product(self, page_name):
        spider = UkSpider()
        response = HtmlResponse(url=page_name,
                                request=Request(url="http://some.url/"),
                                body=self.pages[page_name],
                                encoding='utf-8')
        return spider.parse_product(response)
