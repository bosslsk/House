# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:26
    @subject: 
"""
import os

from local_settings import DevelopmentConfig
from product_settings import ProductionConfig

config = dict(
    default=DevelopmentConfig,
    development=DevelopmentConfig,
    production=ProductionConfig
)

config_name = os.environ.get("MATERIAL_CONFIG_NAME", "default")
config = config[config_name]
