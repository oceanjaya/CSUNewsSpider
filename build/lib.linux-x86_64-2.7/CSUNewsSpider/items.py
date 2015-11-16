# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class NewsItem(Item):
    title=Field()
    date=Field()
    content=Field()
    url=Field()


class AcademicItem(Item):
    title=Field()
    date=Field()
    content=Field()
    location=Field()
    url=Field()
    type=Field()

class JobsItem(Item):
    title=Field()
    date=Field()
    content=Field()
    location=Field()
    url=Field()
    type=Field()

