# -*- coding: utf-8 -*-
import scrapy
# Any additional imports (items, libraries,..)
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from artworks.items import ArtworksItem


class TrialSpider(scrapy.Spider):
    name = "trial"
    start_urls = [
        "http://pstrial-2019-12-16.toscrape.com/browse/insunsh",
        "http://pstrial-2019-12-16.toscrape.com/browse/summertime",
    ]

    def parse(self, response, **kwargs):
        artworks = response.xpath(
            "//*[@id='body']/div//@href[contains(.,'item')]"
        ).getall()
        yield from response.follow_all(artworks, callback=self.parse_art)

        if artworks:
            next_page = response.xpath(
                "//*[@id='body']/div//form[@class='nav next']//@value"
            ).get()
            yield response.follow(f"?page={next_page}", callback=self.parse)

        for subcategory in response.xpath("//*[@id='subcats']/div//@href").getall():
            yield response.follow(subcategory, callback=self.parse)

    @staticmethod
    def parse_art(response):
        artwork = ItemLoader(item=ArtworksItem(), response=response)
        artwork.add_value("url", response.request.url)
        artwork.add_xpath("artist", "//*[@class='artist']/text()")
        artwork.add_xpath("title", "//*[@id='content']/h1/text()")
        artwork.add_xpath("image", "//*[@id='body']/img/@src")
        artwork.add_xpath(
            "width",
            "//*[@class='properties']/tr[contains(td,'Dimensions')]/td[@class='value']",
            TakeFirst(),
            re=r"(\d+\.\d+) x",
        )
        artwork.add_xpath(
            "height",
            "//*[@class='properties']/tr[contains(td,'Dimensions')]/td[@class='value']",
            TakeFirst(),
            re=r"x (\d+\.\d+) cm",
        )
        artwork.add_xpath("description", "//div[@class='description']/p/text()")
        artwork.add_xpath("categories", "//div[@id='content']/a/@href")
        yield artwork.load_item()
