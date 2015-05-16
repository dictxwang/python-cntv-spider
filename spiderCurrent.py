#-*- coding: utf8 -*-
__author__ = 'qiangwang'

from Tools.globalmodule import *
import Tools.finishdog
import Tools.httpexecutor

if __name__ == '__main__':

    print cateCache.convertToName('C10190')
    print configCache.get('user_agent')
    print Tools.finishdog.hasFinished()
    #print Tools.httpexecutor.readHtml('http://tv.cntv.cn/index.php?action=videoset-videolistbytype&class=lanmu&setid=VSET100152389250&istiyu=0&page=12')
    print Tools.httpexecutor.readAndSaveFile('http://vod.cntv.lxdns.com/flash/mp4video41/TMS/wuxi/2015/05/13/b76d9f90b9643ddf588d37a30a4e5c44_h264418000nero_aac32-1.mp4', 'sss.mp4')