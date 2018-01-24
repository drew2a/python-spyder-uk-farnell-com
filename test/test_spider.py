import unittest

from test.test_tool import TestSpider


class TestUkSpider(TestSpider):
    def test_parse_all(self):
        result = self.parse_product('junction_box.html')
        self.assertEqual(
            'junction_box.html',
            result['url'])

        self.assertEqual(
            'RAYTECH',
            result['brand'])

        self.assertEqual(
            ('RAYTECH', 'Junction Box, 46 A, Raytech Gelbox'),
            result['title'])

        self.assertEqual(
            '12.15',
            result['unit_price'])

        self.assertEqual(
            25,
            len(result['overview']))

        self.assertEqual(
            '-',
            result['information']['No. of Ways'])

        self.assertEqual(
            '46A',
            result['information']['Current Rating'])

        self.assertEqual(
            'Raytech Gelbox',
            result['information']['Product Range'])

        self.assertEqual(
            'RAYTECH',
            result['manufacturer'])

        self.assertEqual(
            'KELVIN-MP',
            result['manufacturer_part'].strip())

        self.assertEqual(
            '39231090',
            result['tariff_number'])

        self.assertEqual(
            2,
            len(result['origin_country'].split('\n')))

        self.assertEqual(
            2,
            len(result['files']))

        self.assertEqual(
            1,
            len(result['file_urls']))

        self.assertEqual(
            7,
            len(result['image_urls']))

        self.assertEqual(
            './junction_box_files/EN84834-40.jpg',
            result['primary_image_url'])

        self.assertEqual(
            4,
            len(result['trail']))

    def test_parse_missed_price(self):
        result = self.parse_product('junction_box_no_longer_stocked.html')

        self.assertEqual(
            None,
            result['unit_price'])

    def test_complex_price(self):
        result = self.parse_product('complex_price.html')

        self.assertEqual(
            '2,303.85',
            result['unit_price'])

    def test_video_links(self):
        result = self.parse_product('video_links.html')

        self.assertEqual(
            1,
            len(result['image_urls']))


if __name__ == '__main__':
    unittest.main()
