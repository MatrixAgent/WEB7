# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price1 = scrapy.Field(output_processor=TakeFirst())
    price2 = scrapy.Field(output_processor=TakeFirst())
    unit1 = scrapy.Field(output_processor=TakeFirst())
    price21 = scrapy.Field(output_processor=TakeFirst())
    price22 = scrapy.Field(output_processor=TakeFirst())
    unit2 = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    term = scrapy.Field()
    definition = scrapy.Field(input_processor=MapCompose(lambda s: s.replace('\n', '').strip()))
    spec = scrapy.Field()
    photos = scrapy.Field()
