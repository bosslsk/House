# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:48
    @subject:
"""

import cPickle as pickle

from crawl.utils.date import today_date
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from spider_book.items import MaterialSourceItem
from spider_book.pools import mongo_db


class QidianSourceSpider(RedisSpider):
    name = 'qidian_source'
    redis_key = 'qidian:source'

    def __init__(self, **kwargs):
        super(QidianSourceSpider, self).__init__(**kwargs)
        self.get_books()

    def get_books(self):
        """
        获取起点所有book_id列表，如果抓取新书在此列表中，则不进行重复抓取
        :return:
        """
        books = set(i['book_id'] for i in mongo_db['material_source'].find({'source_id': 1}, {'book_id': 1}))
        self.books = books

    def make_request_from_data(self, data):
        data = pickle.loads(data)
        url = data.pop('data_url', None)
        if url:
            req = Request(
                url,
                meta={'data': data},
                callback=self.parse,
                dont_filter=True
            )
            return req

    def parse(self, response):
        """
        索引列表
        :param response:
        :return:
        """
        data = response.meta['data']
        book_list = response.xpath('//ul[@class="all-img-list cf"]/li')
        for book in book_list:
            url = response.urljoin(book.xpath('./div[2]/h4/a/@href').extract()[0])
            book_id = url.split('/')[-1]
            if book_id in self.books:
                print 'This book is exist'
            yield Request(
                url,
                meta={'data': data},
                callback=self.parse_detail,
                dont_filter=True
            )

    def parse_detail(self, response):
        """
        抓取起点作品详情
        :param response:
        :return:
        """
        data = response.meta['data']
        item = MaterialSourceItem()
        xpath_folder_url = '//div[@class="book-information cf"]/div[@class="book-img"]/a/img/@src'
        xpath_title = '//div[@class="book-information cf"]/div[@class="book-info "]/h1/em/text()'
        xpath_author = '//div[@class="book-information cf"]//a[@class="writer"]/text()'
        xpath_sub_category = '//div[@class="book-information cf"]//a[@class="red"]/text()'
        xpath_introduction = '//div[@class="book-intro"]/p/text()'
        item['url'] = response.url
        item['source_id'] = 1
        item['book_id'] = response.url.split('/')[-1]
        item['relate_id'] = '%s_%s' % (item['source_id'], item['book_id'])
        item['folder_url'] = response.urljoin(response.xpath(xpath_folder_url).extract()[0]).strip()
        item['title'] = response.xpath(xpath_title).extract()[0]
        try:
            item['author'] = response.xpath(xpath_author).extract()[0]
        except IndexError:
            return
        item['tar_category'] = data['tar_category']
        item['source_category'] = data['source_category']
        item['source_category'] = response.xpath(xpath_sub_category).extract()[1]
        introduction = response.xpath(xpath_introduction).extract()
        item['introduction'] = '\n'.join(p.replace(u'　', '').strip() for p in introduction)
        item['created_at'] = today_date()
        item['updated_at'] = today_date()
        yield item
