# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EarthquakeItem(scrapy.Item):
    time_occured = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    magnitude = scrapy.Field()
    depth = scrapy.Field()
    location = scrapy.Field()
