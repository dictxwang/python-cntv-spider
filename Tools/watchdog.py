#-*- coding: utf8 -*-
__author__ = 'qiangwang'

from globalmodule import *
import os
import codecs

def initSotre(cid):
    '''
    根据分类id初始化存储空间
    :param cid:分类编号
    :return:none
    '''
    basedir = configCache.get('base_store')
    ciddir = basedir + '/' + cid
    if not os.path.exists(ciddir):
        os.makedirs(ciddir)
    finisheddir = ciddir + '/finished'
    if not os.path.exists(finisheddir):
        os.makedirs(finisheddir)
    logdir = ciddir + '/logs'
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    videodir = ciddir + '/videos'
    if not os.path.exists(videodir):
        os.makedirs(videodir)
    print 'init store space for %s, dir:%s' % (cid, ciddir)

def hasFinished(cid, vid, isAll, part = 0):
    '''
    判断视频是否已经处理过
    :param cid: 分类编号
    :param vid: 视频编号
    :param isAll: 是否是整个视频信息
    :param part: 视频文件片段编号
    :return:
    '''
    if isAll:
        fPre = 'all_'
        fSuf = ''
        ofPre = 'all_'
    else:
        fPre = 'video_'
        fSuf = '_%d' % part
        ofPre = 'video_%d_' % part
    basedir = configCache.get('base_store')
    ciddir = basedir + '/' + cid
    finishpath = ciddir + '/finished/' + fPre + vid + fSuf +'.finish'
    ofinishpath = ciddir + '/finished/' + ofPre + vid +'.finish'
    if os.path.isfile(finishpath) or os.path.isfile(ofinishpath):
        return True
    else:
        return False

def writeFinished(cid, vInfo, isAll, part = 0):
    '''
    写成功文件
    :param cid: 分类ID
    :param vInfo: 视频信息
    :param isAll: 是否是整个视频信息
    :param part: 视频文件片段编号
    :return:
    '''
    if isAll:
        fPre = 'all_'
        fSuf = ''
    else:
        fPre = 'video_'
        fSuf = '_%d' % part
    basedir = configCache.get('base_store')
    ciddir = basedir + '/' + cid
    finishpath = ciddir + '/finished/' + fPre + vInfo['vid'] + fSuf + '.finish'
    fp = codecs.open(finishpath, mode='w', encoding='utf8')
    if isAll:
        fp.write(vInfo['day'] + '\n')
        fp.write(vInfo['vid'] + '\n')
        fp.write(vInfo['title'] + '\n')
        fp.write(vInfo['image'] + '\n')
    else:
        video = vInfo['videos'][part - 1]
        fp.write(video['duration'] + '\n')
        fp.write(video['url'] + '\n')
    fp.close()
    return True