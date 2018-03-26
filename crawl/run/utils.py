# -*- coding: utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/5 11:31
    @subject:
"""

import redis

from hm_collections.queue.redis_queue import RedisSetQueue

from crawl.settings import config
from crawl.utils.pools import redis_connection_pool
from crawl.run.prepare_data import generate_data as generate_platform_data

r = redis.StrictRedis(connection_pool=redis_connection_pool)


def generate_id_coll(spider_name):
    source, type_ = spider_name.split('_')
    source_id = config.SOURCE_DICT[source]
    data_coll = config.MATERIAL_DICT[type_]
    return source_id, data_coll


def add_data(data, spider_name):
    queue = RedisSetQueue(r, spider_name.replace('_', ':'))
    for i in data:
        queue.push(i)


def generate_data(spider_name, mongo_db, limit=5):
    if spider_name in config.PLATFORM_DATA_SPIDERS:
        data = generate_platform_data(spider_name, mongo_db, limit)
        return data
