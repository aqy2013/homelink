# -*- coding: utf-8 -*-
import scrapy
import re
from itertools import product
from ..items import HomelinkItem
from scrapy.shell import inspect_response
import pymysql
import pymysql.cursors

class HomeSpider(scrapy.Spider):


    name = "home"
    base_url = 'http://sh.lianjia.com'
    allowed_domains = ["sh.lianjia.com"]
    start_urls = []

    # 可筛选条件
    districts = {
        # 'pudongxinqu': '浦东',
         'minhang': '闵行',
        'baoshan': '宝山',
        'xuhui': '徐汇',
        'putuo': '普陀',
        'yangpu': '杨浦',
        'changning': '长宁',
        'songjiang': '松江',
        'jiading': '嘉定',
        'huangpu': '黄浦',
        # 'jingan': '静安',
        # 'zhabei': '闸北',
        # 'hongkou': '虹口',
        # 'qingpu': '青浦',
        # 'fengxian': '奉贤',
        # 'jinshan': '金山',
        # 'chongming': '崇明'
    }
    prices = {
        'z1': '1000-2000元',
        'z2': '2000-4000元',
        'z3': '4000-6000元',
        'z4': '6000-8000元',
        'z5': '8000-12000元',
        'z6': '12000元',
    }
    areas = {
        'a1': '50平以下',
        'a2': '50-70平',
        'a3': '70-90平',
        'a4': '90-110平',
        'a5': '110-130平',
        'a6': '130-150平',
        'a7': '150平以上',
    }
    rooms = {'l1': '一室', 'l2': '二室', 'l3': '三室',
             'l4': '四室', 'l5': '五室', 'l6': '五室以上', }
    faces = {'f1': '东', 'f2': '南', 'f3': '西', 'f4': '北', 'f10': '南北', }
    house_ages = {'y1': '2年内', 'y2': '2-5年',
                  'y3': '5-10年', 'y4': '10-20年', 'y5': '20年以上', }
    floors = {'c1': '低区', 'c2': '中区', 'c3': '高区', }
    decorations = {'x1': '精装', 'x2': '豪装',
                   'x3': '中装', 'x4': '简装', 'x5': '毛坯', }
    brand = {'n1': '链家', 'n2': '自如',}
    kind = {'i1': '整租', 'i2': '合租' ,}
    lable = {'t1': '地铁房', 't3': '随时看', 't4': '降价',}
    # type_keys = product(prices.keys(), areas.keys(), rooms.keys(), faces.keys(), house_ages.keys(),
    #                     floors.keys(), decorations.keys(), brand.keys(), kind.keys() ,lable.keys())
    type_keys = product(prices.keys(), areas.keys())
     # 排列组合所有条件
    # list_urls = {}
    for district in districts:
        for type_key in type_keys:
            url = base_url + '/zufang/' + district + '/' + ''.join(type_key)
            start_urls.append(url)

    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=False
        )
        cursor = self.conn.cursor()
        cursor.execute('select distinct(titileid) from lianjia.data')
        result = cursor.fetchall()


        self.titileids = []
        for item in result:
            self.titileids.append(item[0])

        print self.titileids

    def parse(self, response):

        next_page_url = response.css(
            '.house-lst-page-box a[gahref=results_next_page]::attr(href)').extract_first()
        if next_page_url is not None:
            # 递归下一页
         print u'\r\n※ ※ ※ ※ ※    next page : %s    ※ ※ ※ ※ ※\r\n' % next_page_url
         yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

        item_list = response.css('#house-lst div.info-panel')
        print u'※ ※   current total : %d    ※ ※ ※ ※ ※' % len(item_list)
        for item in item_list:
            xiaoqu = item.css('span.nameEllipsis::text').extract_first()
            property = item.css('div.where > span:nth-child(2)::text').extract_first()
            area = item.css('div.where > span:nth-child(3)::text').extract_first()
            area = re.sub('\D', '', area)
            xqherf = item.css('div.where > a::attr(href)').extract_first()
            xqherf = re.sub('\D', '', xqherf)
            totalcount = item.css('.square .num::text').extract_first()
            url = item.css('h2 > a::attr(href)').extract_first()

            item_href = response.css('#house-lst a[name=selectDetail]::attr(href)').extract_first()
            itid = re.search(r'\d{1,}', item_href).group()

            if itid in self.titileids:
                print u'※ skip : %s    ※ ※ ※ ※ ※' % itid
                pass
            else:
                yield scrapy.Request(self.base_url + url,
                                     meta={'property': property, 'xiaoqu': xiaoqu, 'area': area, 'xqherf': xqherf,
                                           'totalcount': totalcount, 'url': url},
                                     callback=self.parse_detail)

    def parse_detail(self, response):
        # inspect_response(response, self)
        home = HomelinkItem()
        home['title'] = response.css('h1.main::text').extract_first()
        home['avgPrice'] = response.css('div.houseInfo div.price div.mainInfo.bold::text').extract_first()
        home['property'] = response.meta['property']
        home['area'] =  response.meta['area']
        home['xqid'] = response.meta['xqherf']
        home['titileid'] = response.meta['url']
        home['titileid'] = re.sub('\D', '', home['titileid'])
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
