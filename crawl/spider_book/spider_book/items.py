# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    _id = scrapy.Field()
    source_id = scrapy.Field()
    book_id = scrapy.Field()
    relate_id = scrapy.Field()


class MaterialSourceItem(BaseItem):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    folder_url = scrapy.Field()
    tar_category = scrapy.Field()   # 目标分类
    source_category = scrapy.Field()    # 站点分类
    book_status = scrapy.Field()    # 书连载状态  1为完结  0为连载
    introduction = scrapy.Field()
    created_at = scrapy.Field()  # 创建时间
    updated_at = scrapy.Field()  # 更新时间
    chan_id = scrapy.Field()  # 讨论id
    relate_id = scrapy.Field()


class MaterialContentItem(BaseItem):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    relate_id = scrapy.Field()
    tar_category = scrapy.Field()  # 目标分类
    source_category = scrapy.Field()  # 站点分类
    chapter_id = scrapy.Field()  # int
    chapter_name = scrapy.Field()
    download_url = scrapy.Field()
    finished = scrapy.Field()    # 是否成功下载   1 成功   0  失败
    content = scrapy.Field()
    created_at = scrapy.Field()  # 创建时间
    updated_at = scrapy.Field()  # 更新时间
