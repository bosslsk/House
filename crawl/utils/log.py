# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/7 17:44
    @subject: 日志配置
"""

import logging


def get_logger(name, level='DEBUG', log_format=None, filename=None, datefmt=None, **kwargs):
    """建立日志固定方法
    :param name: 打印日志程序名
    :param level: 打印日志等级
    :param log_format: 打印日志格式
    :param filename: 日志存储路径
    :param datefmt: 日志日期保存格式
    :param kwargs:
    :return:
    """
    log_format = log_format or "[%(asctime)s][%(name)s] %(level)s: %(message)s"
    logging.basicConfig(filename=filename, level=level, format=log_format, datefmt=datefmt, **kwargs)
    logger = logging.getLogger(name)

    return logger
