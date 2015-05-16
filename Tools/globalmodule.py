#-*- coding: utf8 -*-
__author__ = 'qiangwang'

import __builtin__
from Tools.category import CateCache
from Tools.config import ConfigCache

#初始化分类
__builtin__.cateCache = CateCache()
#初始化配置
__builtin__.configCache = ConfigCache()