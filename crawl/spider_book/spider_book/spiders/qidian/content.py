# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:48
    @subject:
"""

import json
import cPickle as pickle

from scrapy.conf import settings
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from crawl.utils.binary import str2binary
from crawl.utils.text import text_format
from crawl.utils.date import today_date
from spider_book.items import MaterialContentItem


class QidianContentSpider(RedisSpider):
    name = 'qidian_content'
    redis_key = 'qidian:content'
    download_delay = 2

    def make_request_from_data(self, data):
        """
        反序列化requests_data,调笔趣阁搜索接口
        :param data:
        :return:
        """
        data = pickle.loads(data)
        title = data.get('title', None)
        biquge_url = u'http://www.biquge5200.com/modules/article/search.php?searchkey={searchkey}'
        if title:
            req = Request(
                url=biquge_url.format(searchkey=title),
                meta={'data': data},
                callback=self.parse,
                dont_filter=True
            )
            return req

    def parse(self, response):
        """笔趣阁搜索结果
        :param response:
        :return:
        """
        data = response.meta['data']
        elements = response.xpath('//div[@id="hotcontent"]//tr')[1:]
        if elements:
            for element in elements:
                result_title = element.xpath('./td[@class="odd"]/a/text()').extract()[0]
                print result_title
                result_author = element.xpath('./td[@class="odd"]/text()').extract()[0]
                print result_author
                if result_title == data['title'] and result_author == data['author']:
                    result_url = element.xpath('./td[@class="odd"]/a/@href').extract()[0]
                    yield Request(
                        url=result_url,
                        callback=self.parse_biquge_chapter,
                        meta={'data': data},
                        dont_filter=True
                    )
                    return
        else:
            yield Request(
                url=data['url'],
                meta={'data': data},
                callback=self.parse_qidian,
                dont_filter=True
            )

    def parse_biquge_chapter(self, response):
        """笔趣阁章节列表
        :param response:
        :return:
        """
        if '不存在的网页' in response.body:
            item = response.meta['data']
            yield Request(
                url=item['url'],
                meta={'item': item},
                callback=self.parse_qidian,
                dont_filter=True
            )
        chapters = response.xpath('//div[@id="list"]/dl/dd')[9:]
        chapter_id = 1
        for chapter in chapters:
            item = MaterialContentItem()
            item.update(response.meta['data'])
            item['title'] = chapter.xpath('./a/text()').extract()[0]
            item['ordinal'] = chapter_id
            chapter_url = chapter.xpath('./a/@href').extract()[0]
            item['created_at'] = today_date()
            item['updated_at'] = today_date()
            chapter_id += 1
            yield Request(
                url=chapter_url,
                callback=self.parse_biquge_content,
                meta={'item': item},
                dont_filter=True
            )

    def parse_biquge_content(self, response):
        """笔趣阁章节内容
        :param response:
        :return:
        """
        item = response.meta['item']
        item['chapter_url'] = response.url
        item['content'] = str2binary(text_format(response.xpath('//div[@id="content"]/text()').extract()))
        item['status'] = 1
        yield item

    def parse_qidian(self, response):
        """笔趣阁搜索无结果，则抓取起点免费章节
        :param response:
        :return:
        """
        data = response.meta['data']
        volume_list = response.xpath(u'//div[@class="volume" and not(contains(.,"作品相关"))]')
        if not volume_list:
            self.logger.debug('has 0 volume, now get qidian dynamic chapter list.')
            yield Request(
                'http://book.qidian.com/ajax/book/category?bookId=%s&_csrfToken=' % data['book_id'],
                callback=self.parse_qidian_dynamic,
                meta={'data': data},
                dont_filter=True
            )
        else:
            self.logger.debug('volume list length %s' % len(volume_list))
            for volume in volume_list:
                if volume.xpath('./h3/span/@class').extract()[0] == 'free':
                    chapter_list = volume.xpath('./ul/li')
                    self.logger.debug('chapter list length %s' % len(chapter_list))
                    chapter_id = 1
                    for chapter in chapter_list:
                        # 如果进入到了VIP章节
                        if chapter.xpath('./em[@class="iconfont "]').extract():
                            break
                        chapter_name = chapter.xpath('./a/text()').extract()[0].strip()
                        if any(chapter_name.startswith(w) for w in settings.get('USELESS_CHAPTER')):
                            continue
                        item = MaterialContentItem()
                        item.update(response.meta['data'])
                        item['title'] = chapter_name
                        item['ordinal'] = chapter_id
                        chapter_id += 1
                        chapter_url = response.urljoin(chapter.xpath('./a/@href').extract()[0])
                        yield Request(
                            chapter_url,
                            meta={'item': item},
                            callback=self.parse_qidian_content,
                            dont_filter=True
                        )

    def parse_qidian_dynamic(self, response):
        """
        起点手机端接口
        :param response:
        :return:
        """
        chapter_id = 1
        data = json.loads(response.body)['data']['vs']
        volume_list = data and [d for d in data if d['vN'] != u'作品相关' and d['vS'] == 0] or []
        for volume in volume_list:
            chapter_list = volume['cs']
            for chapter in chapter_list:
                # 如果进入到了VIP章节
                if chapter['sS'] == 0:
                    break
                chapter_name = chapter['cN']
                if any(chapter_name.startswith(w) for w in settings.get('USELESS_CHAPTER')):
                    continue
                item = MaterialContentItem()
                item.update(response.meta['data'])
                item['title'] = chapter_name
                item['ordinal'] = chapter_id
                chapter_id += 1
                chapter_url = 'http://read.qidian.com/chapter/%s' % chapter['cU']
                yield Request(
                    url=chapter_url,
                    meta={'item': item},
                    callback=self.parse_qidian_content,
                    dont_filter=True
                )

    def parse_qidian_content(self, response):
        """
        起点章节内容
        :param response:
        :return:
        """
        item = response.meta['item']
        item['chapter_url'] = response.url
        item['created_at'] = today_date()
        item['updated_at'] = today_date()
        item['content'] = str2binary(text_format(response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()))
        item['status'] = 1
        yield item
