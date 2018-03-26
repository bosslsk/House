# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:23
    @subject: 
"""

import pymongo
import redis

from crawl.settings import config


_client = pymongo.MongoClient(config.MONGO_URI)
mongo_db = _client[config.MONGO_DB_NAME]
_auth = config.MONGO_AUTH

if _auth:
    mongo_db.authenticate(**_auth)

redis_connection_pool = redis.ConnectionPool.from_url(config.REDIS_URL)
