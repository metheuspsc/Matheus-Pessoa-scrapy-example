# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose


def clean_artist(artists):
    if artists:
        return [artist.split(":")[1] for artist in artists.split(";")]


def join_href(href, loader_context):
    return loader_context['response'].urljoin(href)


def split_categories(hrefs):
    return [href for href in hrefs.split("/") if href != 'browse' and href]


class ArtworksItem(scrapy.Item):
    url = scrapy.Field()
    artist = scrapy.Field(input_processor=MapCompose(clean_artist))
    title = scrapy.Field()
    image = scrapy.Field(input_processor=MapCompose(join_href))
    height = scrapy.Field()
    width = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field(input_processor=MapCompose(split_categories))
