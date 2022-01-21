# -*- coding: utf-8 -*-
from types import SimpleNamespace

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
    trial_locators = SimpleNamespace(
        artwork_locator="//*[@id='body']/div//@href[contains(.,'item')]",
        next_page_locator="//*[@id='body']/div//form[@class='nav next']//@value",
        subcategory_locator="//*[@id='subcats']/div//@href",
        artist_locator="//*[@class='artist']/text()",
        title_locator="//*[@id='content']/h1/text()",
        width_locator="//*[@class='properties']/tr[contains(td,'Dimensions')]/td[@class='value']",
        height_locator="//*[@class='properties']/tr[contains(td,'Dimensions')]/td[@class='value']",
        image_locator="//*[@id='body']/img/@src",
        description_locator="//div[@class='description']/p/text()",
        categories_locator="//div[@id='content']/a/@href",
    )

    def parse(self, response, **kwargs):
        artworks = response.xpath(self.trial_locators.artwork_locator).getall()
        yield from response.follow_all(artworks, callback=self.parse_art)
        if artworks:
            yield self.paginate(response)
        yield from self.follow_subcategories(response)

    def paginate(self, response):
        next_page = response.xpath(self.trial_locators.next_page_locator).get()
        return response.follow(f"?page={next_page}", callback=self.parse)

    def follow_subcategories(self, response):
        for subcategory in response.xpath(
            self.trial_locators.subcategory_locator
        ).getall():
            yield response.follow(subcategory, callback=self.parse)

    def parse_art(self, response):
        artwork = ItemLoader(item=ArtworksItem(), response=response)
        artwork.add_value("url", response.request.url)
        artwork.add_xpath("artist", self.trial_locators.artist_locator)
        artwork.add_xpath("title", self.trial_locators.title_locator)
        artwork.add_xpath("image", self.trial_locators.image_locator)
        artwork.add_xpath(
            "width",
            self.trial_locators.width_locator,
            TakeFirst(),
            re=r"(\d+\.\d+) x",
        )
        artwork.add_xpath(
            "height",
            self.trial_locators.height_locator,
            TakeFirst(),
            re=r"x (\d+\.\d+) cm",
        )
        artwork.add_xpath("description", self.trial_locators.description_locator)
        artwork.add_xpath("categories", self.trial_locators.categories_locator)
        yield artwork.load_item()
