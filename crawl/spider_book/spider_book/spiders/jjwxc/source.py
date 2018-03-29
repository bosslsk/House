# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/26 10:12
    @subject: 
"""

import json
import cPickle as pickle
from HTMLParser import HTMLParser

from scrapy import Request, FormRequest
from scrapy_redis.spiders import RedisSpider

from crawl.utils.date import today_date
from spider_book.items import MaterialSourceItem
from spider_book.pools import mongo_db


class JjwxcSourceSpider(RedisSpider):
    name = 'jjwxc_source'
    redis_key = 'jjwxc:source'

    def __init__(self, **kwargs):
        super(JjwxcSourceSpider, self).__init__(**kwargs)
        self.get_books()

    def get_books(self):
        books = set(i['book_id'] for i in list(mongo_db['material_source'].find({'source_id': 7}, {'book_id': 1})))
        self.books = books

    def make_request_from_data(self, data):
        data = pickle.loads(data)
        url = data.pop('data_url')
        if url:
            req = Request(
                url=url,
                meta={'data': data},
                callback=self.parse,
                dont_filter=True
            )
            return req

    def parse(self, response):
        book_list = response.xpath('//table[@class="cytable"]/tbody/tr')[1:]
        for book in book_list:
            item = MaterialSourceItem()
            item.update(response.meta['data'])
            href = book.xpath('./td[2]/a/@href').extract()[0]
            book_id = href.split('=')[1]
            item['book_id'] = book_id
            if book_id in self.books:
                item['relate_id'] = '%s_%s' % (item['source_id'], item['book_id'])
                yield item
                continue
            book_url = 'http://app.jjwxc.org/androidapi/novelbasicinfo?novelId={}'.format(book_id)
            yield FormRequest(
                book_url,
                formdata={'versionCode': '75'},
                meta={'item': item},
                callback=self.parse_detail,
                dont_filter=True
            )

    def parse_detail(self, response):
        try:
            detail_json = json.loads(response.body)
        except ValueError:
            self.logger.error('[NO JSON]' + response.url)
            with open('no_json_decoded.log', 'w') as f:
                f.write(response.body)
            return
        if 'code' in detail_json:
            return
        clock = int(detail_json['islock'])
        if clock:
            self.logger.debug('[THIS BOOK IS CLOCK] ' + response.url)
            return
        item = MaterialSourceItem()
        item.update(response.meta['item'])
        item['relate_id'] = '%s_%s' % (item['source_id'], item['book_id'])
        item['url'] = 'http://www.jjwxc.net/onebook.php?novelid={}'.format(item['book_id'])
        item['folder_url'] = detail_json['novelCover']
        item['title'] = detail_json['novelName']
        item['author'] = detail_json['authorName']
        item['gender'] = u'女性向小说'
        introduction = HTMLParser().unescape(detail_json['novelIntro'])
        item['introduction'] = '\n'.join(p.strip() for p in introduction.split('<br/>') if p != '')
        item['created_at'] = today_date()
        item['updated_at'] = today_date()
        yield item
