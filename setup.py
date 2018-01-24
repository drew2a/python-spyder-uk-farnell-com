from setuptools import setup, find_packages

setup(
    name='spyder_uk_farnell_com',
    version='1.10',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = spyder_uk_farnell_com.settings']},
    package_data={
        'spyder_uk_farnell_com': ['resources/*.txt']
    },
    zip_safe=False
)
