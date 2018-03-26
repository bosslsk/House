# -*- coding: utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/5 11:20
    @subject:
"""

import redis

from hm_collections.queue.redis_queue import RedisSetQueue

from crawl.run.utils import generate_id_coll, generate_data
from crawl.utils.pools import redis_connection_pool, mongo_db
from crawl.utils.date import today_date

r = redis.StrictRedis(connection_pool=redis_connection_pool)


def add_data(data, spider_name):
    """
    将spider启动所需数据加入redis队列
    :param data:
    :param spider_name:
    :return:
    """
    queue = RedisSetQueue(r, spider_name.replace('_', ':'))
    for i in data:
        queue.push(i)


def remove_queue_data(spider_name):
    """
    清空redis中的相关key
    :param spider_name:
    :return:
    """
    queue = RedisSetQueue(r, spider_name.replace('_', ':'))
    queue.flush()
    queue = RedisSetQueue(r, spider_name + ':requests')
    queue.flush()


def remove_mongo_data(spider_name):
    """
    清空mongodb中的相关数据
    :param spider_name:
    :return:
    """
    source_id, data_coll = generate_id_coll(spider_name)
    if source_id <= 21:
        mongo_db[data_coll].remove({'source_id': source_id, 'updated_at': today_date()})
    else:
        mongo_db[data_coll].remove({})


def start_ceshi(spider_name, limit=5, **kwargs):
    """
    测试前的数据准备
    :param spider_name: 爬虫 project name
    :param limit: 索引
    :param kwargs:
    :return:
    """
    data = generate_data(spider_name, mongo_db, limit=limit, **kwargs)
    remove_queue_data(spider_name)
    remove_mongo_data(spider_name)
    add_data(data, spider_name)
