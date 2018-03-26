# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/5 11:17
    @subject: 
"""

from argparse import ArgumentParser

from crawl.run.ceshi.utils import start_ceshi

parser = ArgumentParser()
parser.add_argument('spider')
parser.add_argument('limit')

args = parser.parse_args()
spider = args.spider
limit = int(args.limit)

start_ceshi(args.spider, int(args.limit))
