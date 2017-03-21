# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

class HomelinkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def get_latitude(source):
        listdata = re.findall('[0-9]*\.?[0-9]+', source[0])
        return [listdata[1]]

    def get_longitude(source):
        listdata = re.findall('[0-9]*\.?[0-9]+', source[0])
        return [listdata[0]]

    def get_build_year(source):
        source[0] = re.sub(u'(\\n|\\t|\ |年)', '', source[0])
        return source

    def remove_useless_tag(source):
        result = ''
        for item in source:
            result += re.sub('(\\t\\n|\\n|\\t| )', '', item)
        return [result]

    title = scrapy.Field()
    address = scrapy.Field(output_processor=remove_useless_tag)
    avgPrice = scrapy.Field(output_processor=remove_useless_tag)
    property = scrapy.Field(output_processor=remove_useless_tag)
    area = scrapy.Field(output_processor=remove_useless_tag)
    chaoxiang =scrapy.Field(output_processor=remove_useless_tag)
    louceng = scrapy.Field(output_processor=remove_useless_tag)
    sjtime =scrapy.Field(output_processor=remove_useless_tag)
    xiaoqu = scrapy.Field(output_processor=remove_useless_tag)
    quyu = scrapy.Field(output_processor=remove_useless_tag)
    count = scrapy.Field(output_processor=remove_useless_tag)
    xqid = scrapy.Field()
    titileid = scrapy.Field()
    totalcount = scrapy.Field()
