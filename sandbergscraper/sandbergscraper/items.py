# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class estateItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    build_area = scrapy.Field()
    plot_size = scrapy.Field()
    bath_rooms = scrapy.Field()
    bed_rooms = scrapy.Field()
    description = scrapy.Field()
    location_desc = scrapy.Field()
    

