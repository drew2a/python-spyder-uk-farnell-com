# -*-
#  coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from collections import defaultdict

from spyder_uk_farnell_com.items import Product


class UkSpider(scrapy.Spider):
    name = 'uk_farnell_com_spider'
    allowed_domains = ['farnell.com']

    def start_requests(self):
        yield scrapy.Request(
            'http://uk.farnell.com/c/electrical/prl/results',
            self.parse)

        yield scrapy.Request(
            'http://uk.farnell.com/c/engineering-software/prl/results',
            self.parse)

        yield scrapy.Request(
            'http://uk.farnell.com/c/wireless-modules-adaptors/prl/results',
            self.parse)

    def parse(self, response):
        product_urls = response.css(
            '#sProdList > tbody > tr > td.productImage.mftrPart > a::attr(href)'
        ).extract()

        for product_url in product_urls:
            yield scrapy.Request(product_url, self.parse_product)

        next_page_url = response.css(
            'span.paginNextArrow > a::attr(href)'
        ).extract_first()

        if next_page_url:
            yield scrapy.Request(next_page_url, self.parse)

    def parse_product(self, response):
        legislation_dictinary = UkSpider.create_legislation_dictionary(
            response.css(
                '#pdpSection_ProductLegislation > div.collapsable-content > dl'
            ).extract_first()
        )

        brand = response.css(
            'span.schemaOrg[itemprop="http://schema.org/brand"]::text'
        ).extract_first()

        title = response.css(
            'div.mainPdpWrapper > section:nth-child(4) > h2 > span::text'
        ).extract_first()

        product = Product(
            url=response.url,
            brand=brand,
            title=(brand, title),
            tariff_number=legislation_dictinary['tariff no:'],
            origin_country=legislation_dictinary['country of origin:'],
            unit_price=response.css(
                'div.availabilityPriceContainer > div.inventoryStatus > div.productPrice > span.price::text'
            ).re_first(r'[\d\.,]+'),

            overview=response.css(
                '#pdpSection_FAndB > div.collapsable-content *::text'
            ).extract(),

            information=UkSpider.parse_information_table(
                response.css('#pdpSection_pdpProdDetails > div.collapsable-content')
            ),

            manufacturer=response.css(
                'span[itemprop="http://schema.org/manufacturer"]::text'
            ).extract_first(),

            manufacturer_part=response.css(
                'dd[itemprop="mpn"]::text'
            ).extract_first(),

            files=response.css(
                '#technicalData a::text'
            ).extract(),

            file_urls=response.css(
                '#technicalData a::attr(href)'
            ).extract(),

            image_urls=response.css(
                '#thumbsContainer > div.mediaThumbsScroller img::attr(src)'
            ).extract(),

            primary_image_url=response.css(
                '#productMainImage::attr(src)'
            ).extract_first(),

            trail=response.css(
                '#breadcrumb > nav a::text'
            ).extract()
        )

        return product

    @staticmethod
    def create_legislation_dictionary(html):
        dictionary = defaultdict(lambda: None)
        if not html:
            return dictionary

        soup = BeautifulSoup(html, features='html.parser')
        for dt, dd in zip(soup.findAll('dt'), soup.findAll('dd')):
            key = dt.text.strip().lower()
            value = dd.text.strip()

            dictionary[key] = value

        return dictionary

    @staticmethod
    def parse_information_table(css_selector):
        table = dict()
        attributes = css_selector.css('dt::attr(id)').extract()
        for attribute_name in attributes:
            attribute_value = attribute_name.replace("Name", "Value")

            key = css_selector.css(
                'dt[id~=%s] label::text' % attribute_name
            ).extract_first()

            value = css_selector.css(
                'dd[id~=%s] a::text' % attribute_value
            ).extract_first()

            table[key] = value

        return table
