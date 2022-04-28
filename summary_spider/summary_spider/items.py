# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SummarySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    ts = scrapy.Field()
    origin_url = scrapy.Field()
    summary_url = scrapy.Field()
    publish_time = scrapy.Field()
    website = scrapy.Field()


