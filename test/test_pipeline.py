import unittest

from spyder_uk_farnell_com.items import Product
from spyder_uk_farnell_com.pipelines import OmitFieldPipeline, ItemPostProcessPipeline
from test.test_tool import TestSpider


class TestPipeline(TestSpider):
    def test_omit_field_pipeline(self):
        product = Product(
            title='title',
            brand='brand')

        omit_field_pipeline = OmitFieldPipeline()
        self.assertEqual(
            2,
            len(product.keys()))

        self.assertEqual(
            2,
            len(omit_field_pipeline.process_item(product, None).keys()))

        product['title'] = None
        self.assertEqual(
            2,
            len(product.keys()))

        self.assertEqual(
            1,
            len(omit_field_pipeline.process_item(product, None).keys()))

    def test_item_post_process_pipeline(self):
        product = self.parse_product('junction_box.html')

        product = OmitFieldPipeline().process_item(product, None)
        product = ItemPostProcessPipeline().process_item(product, None)

        self.assertEqual(
            'junction_box.html',
            product['url'])

        self.assertEqual(
            'RAYTECH',
            product['brand'])

        self.assertEqual(
            'RAYTECH Junction Box, 46 A, Raytech Gelbox',
            product['title'])

        self.assertEqual(
            12.15,
            product['unit_price'])

        self.assertEqual(
            370,
            len(product['overview']))

        self.assertEqual(
            '-',
            product['information']['No. of Ways'])

        self.assertEqual(
            '46A',
            product['information']['Current Rating'])

        self.assertEqual(
            'Raytech Gelbox',
            product['information']['Product Range'])

        self.assertEqual(
            'RAYTECH',
            product['manufacturer'])

        self.assertEqual(
            'KELVIN-MP',
            product['manufacturer_part'].strip())

        self.assertEqual(
            '39231090',
            product['tariff_number'])

        self.assertEqual(
            'Italy',
            product['origin_country'])

        self.assertEqual(
            1,
            len(product['files']))

        self.assertEqual(
            'Technical Data Sheet EN',
            product['files'][0])

        self.assertEqual(
            1,
            len(product['file_urls']))

        self.assertEqual(
            'http://www.farnell.com/datasheets/2025605.pdf',
            product['file_urls'][0])

        self.assertEqual(
            7,
            len(product['image_urls']))

        self.assertEqual(
            './junction_box_files/EN84834-40.jpg',
            product['image_urls'][0])

        self.assertEqual(
            './junction_box_files/EN84834-40.jpg',
            product['primary_image_url'])

        self.assertEqual(
            2,
            len(product['trail']))

        self.assertEqual(
            'Electrical',
            product['trail'][0])

    def test_complex_price(self):
        product = self.parse_product('complex_price.html')
        pipeline = ItemPostProcessPipeline()
        postprocessed_product = pipeline.process_item(product, None)

        self.assertEqual(
            2303.85,
            postprocessed_product['unit_price'])

    def test_360_links(self):
        product = self.parse_product('360_link.html')
        pipeline = ItemPostProcessPipeline()
        postprocessed_product = pipeline.process_item(product, None)

        self.assertEqual(
            3,
            len(postprocessed_product['image_urls']))


if __name__ == '__main__':
    unittest.main()
