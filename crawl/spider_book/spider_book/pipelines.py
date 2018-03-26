# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider_book.pools import mongo_db


class SpiderBookPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'qidian_source':
            mongo_db['material_source'].update_one(
                {'_id': item['relate_id']},
                {'$set': item},
                upsert=True
            )
        if spider.name == 'qidian_content':
            item['_id'] = '%s_%s' % (item['relate_id'], item['chapter_id'])
            mongo_db['material_content'].update_one(
                {'_id': item['_id']},
                {'$set': item},
                upsert=True
            )
        return item
