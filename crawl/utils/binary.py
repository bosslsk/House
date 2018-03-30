# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/28 14:59
    @subject: 
"""

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from bson import Binary


def str2binary(data):
    """字符串转为二进制格式
    :param data:
    :return:
    """
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return Binary(StringIO(data).getvalue())
