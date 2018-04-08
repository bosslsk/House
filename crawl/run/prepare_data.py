# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/5 12:01
    @subject: 
"""

from crawl.settings import config


def generate_id_coll(spider_name):
    """
    获取站点和数据库表名
    :param spider_name:
    :return:
    """
    source, type_ = spider_name.split('_')
    source_id = config.SOURCE_DICT[source]
    data_coll = config.MATERIAL_DICT[type_]
    return source_id, data_coll


def collect_data(spider_name, mongodb, limit=0):
    """
    构造数据
    :param spider_name:
    :param mongodb: 数据库连接池
    :param limit:
    :return:
    """
    source_id, data_coll = generate_id_coll(spider_name)
    param = {
        '_id': 0, 'source_id': 1, 'book_id': 1, 'relate_id': 1, 'title': 1, 'url': 1, 'author': 1
    }
    if 'index' in data_coll:
        start_url_info = config.SOURCE_START_URL_DICT[spider_name.split('_')[0]]
        data = source_data(source_id, start_url_info)
    elif data_coll == 'jjwxc_content':
        category_list = list(mongodb['material_index'].aggregate(
            [
                {'$match': {'source_id': 7}},
                {'$project': {'_id': 0, 'source_category': 1}},
                {'$unwind': {'path': '$source_category', 'preserveNullAndEmptyArrays': True, }},
                {'$group': {'_id': '$source_category'}}
            ]
        ))
        data = []
        for source_category in category_list:
            data.extend(list(mongodb['material_index'].find({'source_id': 7, 'source_category': source_category['_id']}, param).sort([('sort', 1)]).limit(20)))
    else:
        data = list(mongodb['material_index'].find({'source_id': source_id}, param).limit(limit))
    return data


def source_data(source_id, start_url_info):
    """
    不同站点request_data的构造
    :param source_id:
    :param start_url_info:
    :return:
    """
    data = []
    for tar in start_url_info['tag'].keys():
        tar_category = tar
        for sub in start_url_info['tag'][tar]:
            source_category = sub.split('#')[0]
            if source_id == 1:
                chanId = sub.split('#')[1].split('_')[0]
                subCateId = sub.split('#')[1].split('_')[1]
                data_info = {
                    'data_url': start_url_info['url'].format(chanId=chanId, subCateId=subCateId),
                    'source_id': source_id,
                    'tar_category': tar_category,
                    'source_category': source_category

                }
                data.append(data_info)
            if source_id == 7:
                bq = sub.split('#')[1]
                data_info = {
                    'data_url': start_url_info['url'].format(bq=bq),
                    'source_id': source_id,
                    'tar_category': tar_category,
                    'source_category': source_category
                }
                data.append(data_info)
    return data
