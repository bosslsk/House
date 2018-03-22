# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:04
    @subject: 
"""


class Config(object):
    MATERIAL_SOURCE = 'material_source'
    MATERIAL_CONTENT = 'material_content'

    SOURCE_DICT = {
        'qidian': 1,
        'jjwxc': 7
    }


class DevelopmentConfig(object):
    # mongodb
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB_NAME = 'htf_spider'
    MONGO_AUTH = {}

    # redis
    REDIS_URI = 'redis://localhost:6379/4'
