#-*- coding: utf8 -*-
__author__ = 'qiangwang'

import ConfigParser


class ConfigCache:

    def __init__(self):
        self._config_ = self._parseConfig_()

    def getConfigs(self):
        return self._config_

    def get(self, key):
        if key is None or not self._config_.has_key(key):
            return None
        return self._config_[key]

    def _parseConfig_(self):
        cp = ConfigParser.ConfigParser()
        fp = open('CONF/common.ini', 'r')
        cp.readfp(fp)
        config = {}
        config['use_proxy'] = int(cp.get('http', 'use_proxy'))
        config['proxy_address'] = cp.get('http', 'proxy_address')
        config['user_agent'] = cp.get('http', 'user_agent')

        config['base_store'] = cp.get('task', 'base_store')
        config['spider_cate'] = cp.get('task', 'spider_cate')
        config['max_page'] = int(cp.get('task', 'max_page'))

        fp.close()
        print 'parse configuration done.'
        return config
