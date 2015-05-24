#-*- coding: utf8 -*-
__author__ = 'qiangwang'

import ConfigParser
import os


class ConfigCache:

    def __init__(self):
        self._config_ = self._parseConfig_()

    def getConfigs(self):
        return self._config_

    def get(self, key):
        if key is None or not self._config_.has_key(key):
            return None
        return self._config_[key]

    def set(self, key, value):
        if key is not None and value is not None:
            self._config_[key] = value

    def _parseConfig_(self):
        cp = ConfigParser.ConfigParser()
        fp = open('CONF/common.ini', 'r')
        cp.readfp(fp)
        config = {}
        config['use_proxy'] = int(cp.get('http', 'use_proxy'))
        config['proxy_address'] = cp.get('http', 'proxy_address').split(',')
        config['user_agent'] = cp.get('http', 'user_agent')

        config['base_store'] = cp.get('task', 'base_store')

        if not os.path.exists(config['base_store']):
            #如果设置的存储位置不存在，强制保存到脚本所在路径
            basedir = 'STORE'
            basedir = os.path.abspath(basedir)
            config['base_store'] = basedir
            print '[Warn] configuration base_store error, the direction is not exists'
        config['spider_cate'] = cp.get('task', 'spider_cate')
        config['max_page'] = int(cp.get('task', 'max_page'))

        fp.close()
        print 'parse configuration done.'
        return config
