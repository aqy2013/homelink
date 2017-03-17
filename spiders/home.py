# -*- coding: utf-8 -*-
import scrapy
import re
import string
from ..items import HomelinkItem
from scrapy.shell import inspect_response


class HomeSpider(scrapy.Spider):
    name = "home"
    base_url = 'http://sh.lianjia.com'
    allowed_domains = ["sh.lianjia.com"]
    start_urls = [base_url + '/zufang']

    def parse(self, response):
        item_list = response.css('#house-lst div.info-panel')
        print u'※ ※ ※ ※ ※    current total : %d    ※ ※ ※ ※ ※' % len(item_list)
        for item in item_list:
            xiaoqu = item.css('span.nameEllipsis::text').extract_first()
            property = item.css('div.where > span:nth-child(2)::text').extract_first()
            area = item.css('div.where > span:nth-child(3)::text').extract_first()
            area = re.sub('\D', '', area)
            xqherf = item.css('div.where > a::attr(href)').extract_first()
            xqherf = re.sub('\D','',xqherf)
            totalcount = item.css('.square .num::text').extract_first()
            url = item.css('h2 > a::attr(href)').extract_first()
            yield scrapy.Request(self.base_url + url, meta={'property': property, 'xiaoqu': xiaoqu , 'area': area ,'xqherf':xqherf ,'totalcount':totalcount},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        home = HomelinkItem()
        # inspect_response(response, self)
        home['title'] = response.css('h1.main::text').extract_first()
        home['avgPrice'] = response.css('div.houseInfo div.price div.mainInfo.bold::text').extract_first()
        home['property'] = response.meta['property']
        home['area'] =  response.meta['area']
        home['xqid'] = response.meta['xqherf']
        home['totalcount'] = response.meta['totalcount']
        home['louceng'] = response.css(
            'body > div.zf-top > div.cj-cun > div.content.forRent > table > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
        home['louceng'] = re.sub('(\\t\\n|\\n|\\t|\ )', '', home['louceng'])
        home['chaoxiang'] = response.css(
            'body > div.zf-top > div.cj-cun > div.content.forRent > table > tr:nth-child(1) > td:nth-child(4)::text').extract_first()
        home['chaoxiang'] = re.sub('(\\t\\n|\\n|\\t|\ )', '', home['chaoxiang'])
        home['quyu'] = response.css(
            'body > div.zf-top > div.cj-cun > div.content.forRent > table > tr:nth-child(2) > td:nth-child(2)::text').extract_first()
        home['quyu'] = re.sub('(\\t\\n|\\n|\\t|\ )', '', home['quyu'])
        home['sjtime'] = response.css(
            'body > div.zf-top > div.cj-cun > div.content.forRent > table > tr:nth-child(2) > td:nth-child(4)::text').extract_first()
        home['sjtime'] = re.sub('(\\t\\n|\\n|\\t|\ )', '', home['sjtime'])
        home['xiaoqu'] = response.meta['xiaoqu']
        home['address'] = response.css(
            'body > div.zf-top > div.cj-cun > div.content.forRent > table > tr:nth-child(4) > td:nth-child(2)>p::text').extract_first()
        home['address'] = re.sub('(\\t\\n|\\n|\\t|\ )', '', home['address'])
        home['count'] = response.css('.record .panel .count::text').extract_first()
        home['count'] = re.sub('(\\t\\n|\\n|\\t|\ )', '', home['count'])
        return home
