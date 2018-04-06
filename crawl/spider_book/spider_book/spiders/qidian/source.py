# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:48
    @subject:
"""

import cPickle as pickle

from crawl.utils.date import today_date, now_date
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
        books = set(i['book_id'] for i in mongo_db['material_index'].find({'source_id': 1}, {'book_id': 1}))
        self.books = books

    def make_request_from_data(self, data):
        """
        反序列化request_data，构造请求链接
        :param data:
        :return:
        """
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
        获取起点索引列表
        :param response:
        :return:
        """
        book_list = response.xpath('//ul[@class="all-img-list cf"]/li')
        for book in book_list:
            item = MaterialSourceItem()
            item.update(response.meta['data'])
            url = response.urljoin(book.xpath('./div[2]/h4/a/@href').extract()[0])
            book_id = url.split('/')[-1]
            item['book_id'] = book_id
            if book_id in self.books:
                item['relate_id'] = '%s_%s' % (item['source_id'], item['book_id'])
                yield item
                continue
            yield Request(
                url,
                meta={'item': item},
                callback=self.parse_detail,
                dont_filter=True
            )

    def parse_detail(self, response):
        """
        抓取起点作品详情
        :param response:
        :return:
        """
        item = response.meta['item']
        xpath_folder_url = '//div[@class="book-information cf"]/div[@class="book-img"]/a/img/@src'
        xpath_title = '//div[@class="book-information cf"]/div[@class="book-info "]/h1/em/text()'
        xpath_author = '//div[@class="book-information cf"]//a[@class="writer"]/text()'
        xpath_introduction = '//div[@class="book-intro"]/p/text()'
        item['url'] = response.url
        item['relate_id'] = '%s_%s' % (item['source_id'], item['book_id'])
        item['folder_url'] = response.urljoin(response.xpath(xpath_folder_url).extract()[0]).strip()
        item['title'] = response.xpath(xpath_title).extract()[0]
        try:
            item['author'] = response.xpath(xpath_author).extract()[0]
        except IndexError:
            return
        item['gender'] = u'男性向小说'
        introduction = response.xpath(xpath_introduction).extract()
        item['introduction'] = '\n'.join(p.replace(u'　', '').strip() for p in introduction)
        item['created_at'] = now_date()
        item['updated_at'] = today_date()
        yield item
