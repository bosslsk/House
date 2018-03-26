# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 14:31
    @subject: 
"""

from datetime import datetime


def today_date():
    now = datetime.now()
    return datetime(now.year, now.month, now.day)
