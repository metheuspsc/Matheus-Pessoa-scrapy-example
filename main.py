from scrapy import cmdline

cmdline.execute("scrapy crawl trial -o artworks.csv".split())
