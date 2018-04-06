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


def now_date():
    now = datetime.now()
    return datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
