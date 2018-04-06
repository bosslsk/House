# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider_book.pools import mongo_db


class SpiderBookPipeline(object):
    def process_item(self, item, spider):
        print item
        if spider.name in ['qidian_source', 'jjwxc_source']:
            source_category = item.pop('source_category')
            mongo_db['material_index'].update_one(
                {'_id': item['relate_id']},
                {'$set': item, '$addToSet': {'source_category': source_category}},
                upsert=True
            )
        if spider.name in ['qidian_content', 'jjwxc_content']:
            item.pop('author', None)
            item.pop('url', None)
            item['_id'] = '%s_%s' % (item['relate_id'], item['ordinal'])
            item['text_url'] = '%s/%s' % (item['book_id'], item['ordinal'])
            mongo_db['material_chapter'].update_one(
                {'_id': item['_id']},
                {'$set': item},
                upsert=True
            )
        return item
