# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/2/28 16:24
    @subject: mongo连接池
"""

import redis
import pymongo

from scrapy.conf import settings

_client = pymongo.MongoClient(settings.get('MONGO_URI'))
mongo_db = _client[settings.get('MONGO_DB_NAME')]
_auth = settings.get('MONGO_AUTH')
if _auth:
    mongo_db.authenticate(**_auth)

redis_connection_pool = redis.ConnectionPool.from_url(settings.get("REDIS_URL"))
