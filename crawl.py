from scrapy import cmdline

cmdline.execute("scrapy crawl uk_farnell_com_spider -o results.jl".split())
