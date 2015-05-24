#-*- coding: utf8 -*-
__author__ = 'qiangwang'

from Tools.globalmodule import *
import Tools.watchdog
import Tools.httpexecutor
from Tools.currentprocessor import doCategorySiper
from multiprocessing import Process

if __name__ == '__main__':

    cates = configCache.get('spider_cate').split(',')
    if not cates or len(cates) == 0:
        print 'no category, job exit...'
        exit()

    #初始化存储空间，其他任务执行的必要过程
    for cate in cates:
        Tools.watchdog.initSotre(cate)

    #以下开始多进程并行执行，每个分类一个进程
    for cate in cates:
        p = Process(target=doCategorySiper, args=(cate, configCache.get('max_page')))
        p.start()