#-*- coding: utf8 -*-
__author__ = 'qiangwang'

from globalmodule import *
import urllib2
import random


def readHtml(url):
    '''
    获取静态页面源码
    :param url:
    :return:
    '''
    try:
        request = urllib2.Request(url)
        request.add_header("User-Agent", configCache.get('user_agent'))

        proxy_handler = {}
        opener = None
        if configCache.get('use_proxy') == 1:
            #随机选择一个代理地址
            random.shuffle(configCache.get('proxy_address'))
            proxy_handler = urllib2.ProxyHandler({'http': configCache.get('proxy_address')[0]})
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener()
        res = opener.open(request)
        return res.read()
    except:
        return None

def readAndSaveFile(url, filepath):
    '''
    请求url，保存stream文件
    :param url:
    :param fp:
    :return:
    '''
    try:
        request = urllib2.Request(url)
        request.add_header("User-Agent", configCache.get('user_agent'))

        proxy_handler = {}
        opener = None
        if configCache.get('use_proxy') == 1:
            random.shuffle(configCache.get('proxy_address'))
            proxy_handler = urllib2.ProxyHandler({'http': configCache.get('proxy_address')[0]})
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener()
        res = opener.open(request)
        fp = open(filepath, 'wb')
        meta = res.info()
        if meta is not None and meta.getheader('Content-Length') is not None:
            length = int(meta.getheader('Content-Length'))
            buffer = None
            while True:
                buffer = res.read(8192)
                if buffer is None or len(buffer) == 0:
                    break
                fp.write(buffer)

        else:
            fp.write(res.read())
        fp.close()
        print '[OK] save file:%s' % filepath
        return True
    except:
        return False