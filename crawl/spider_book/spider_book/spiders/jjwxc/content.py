# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/26 18:44
    @subject: 
"""

import cPickle as pickle

from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from crawl.utils.binary import str2binary
from crawl.utils.date import today_date
from crawl.utils.text import text_format
from spider_book.items import MaterialContentItem


class JjwxcContentSpider(RedisSpider):
    name = 'jjwxc_content'
    redis_key = 'jjwxc:content'

    def make_request_from_data(self, data):
        """
        获取request_data，请求搜狗小说网作品搜索接口
        :param data:
        :return:
        """
        data = pickle.loads(data)
        title = data.get('title', None)
        sougou_url = u'http://www.sgxsw.com/s.php?ie=gbk&q={q}'
        if title:
            req = Request(
                url=sougou_url.format(q=title),
                meta={'data': data},
                callback=self.parse_sougou,
                dont_filter=True
            )
            return req

    def parse_sougou(self, response):
        """
        搜狗小说网按书名搜索，并匹配书名和作者
        :param response:
        :return:
        """
        item = MaterialContentItem()
        item.update(response.meta['data'])
        elements = response.xpath('//div[@class="bookbox"]')
        if not elements:
            # 搜索无结果
            return
        for element in elements:
            result_title = element.xpath('.//h4[@class="bookname"]/a/text()').extract()[0]
            result_author = element.xpath('.//div[@class="author"]/text()').extract()[0].split(u'：')[1]
            if result_title == item['title'] and result_author == item['author']:
                result_url = response.urljoin(element.xpath('.//h4[@class="bookname"]/a/@href').extract()[0])
                yield Request(
                    url=result_url,
                    callback=self.parse_sougou_chapter,
                    meta={'item': item},
                    dont_filter=True
                )
                return

    def parse_sougou_chapter(self, response):
        """
        搜狗小说网章节列表
        :param response:
        :return:
        """
        chapters = response.xpath('//div[@class="listmain"]/dl/dd')
        chapter_id = 1
        for chapter in chapters:
            item = MaterialContentItem()
            item.update(response.meta['item'])
            try:
                item['title'] = chapter.xpath('./a/text()').extract()[0]
            except IndexError:
                item['title'] = chapter.xpath('.//b/text()').extract()[0]
            item['ordinal'] = chapter_id
            chapter_id += 1
            item['created_at'] = today_date()
            item['updated_at'] = today_date()
            chapter_url = response.urljoin(chapter.xpath('./a/@href').extract()[0])
            yield Request(
                url=chapter_url,
                meta={'item': item},
                callback=self.parse_sougou_content,
                dont_filter=True
            )

    def parse_sougou_content(self, response):
        """
        搜狗小说网内容抓取
        :param response:
        :return:
        """
        item = response.meta['item']
        item['chapter_url'] = response.url
        item['content'] = str2binary(text_format(response.xpath('//div[@id="content"]/text()').extract()))
        item['status'] = 1
        yield item
