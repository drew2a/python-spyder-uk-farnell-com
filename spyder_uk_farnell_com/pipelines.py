from spyder_uk_farnell_com.items import Product


class ItemPostProcessPipeline(object):
    def __init__(self):
        self.handlers = {
            'overview':
                lambda field: '\n'.join(remove_empty_lines(field)),
            'files':
                lambda field: list(remove_empty_lines(field)),
            'unit_price':
                lambda field: float(field.replace(',', '')),
            'origin_country':
                lambda field: field.split('\n')[0].strip(),
            'trail':
                lambda field: field[1:-1],
            'manufacturer_part':
                lambda field: field.strip(),
            'title':
                lambda field: '{0} {1}'.format(
                    (field[0] or ''),
                    (field[1] or '')
                ).strip(),
            'image_urls':
                lambda field: [image_url for image_url in field
                               if not image_url.endswith('360icon.png')]}

    def process_item(self, item, spider):
        for key in item.keys():
            if key in self.handlers:
                item[key] = self.handlers[key](item[key])

        return item


class OmitFieldPipeline(object):
    def process_item(self, item, spider):
        return Product((key, item[key]) for key in item.keys() if item[key])


def remove_empty_lines(lines):
    return filter(lambda l: l is not '',
                  map(lambda line: line.strip(), lines))
