#-*- coding: utf8 -*-
__author__ = 'wangqiang'

from Tools.globalmodule import *
import time
import re
import json
from Tools.httpexecutor import *
import Tools.watchdog


def getVideoIdList(cid, page):
    '''
    分页查找video的信息
    :param cid: 分类编号
    :param page: 页码
    :return:视频ID的list（保证视频的顺序和源站一致）
    '''
    urlprefix = 'http://tv.cntv.cn/index.php?action=videoset-videolistbytype&class=lanmu&istiyu=0'
    if not cid or len(cid) == 0:
        return None
    if page < 1:
        page = 1
    url = urlprefix + '&setid=' + cid + '&page=' + str(page)
    #最多重试三次
    count = 0
    while count < 3:
        html = readHtml(url)
        if html is not None:
            break
        count += 1
        time.sleep(0.1 * count)

    if html is None:
        return None
    matches = re.findall(r'<h3>.*</h3>', html)
    if matches is not None and len(matches) > 0:
        result = []
        for m in matches:
            m = m.replace('<h3><a href="/video/'+cid+'/', '')
            m = m.replace('</a></h3>', '')
            parts = m.split('">')
            if parts is not None and len(parts) == 2:
                result.append(parts[0])
        return result
    else:
        return None

def getVideoInfo(vid):
    urlprefix = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?modifyed=false&pid='
    if vid is None or len(vid) == 0:
        return None
    url = urlprefix + vid
    #最多重试三次
    count = 0
    while count < 3:
        html = readHtml(url)
        if html is not None:
            break
        count += 1
        time.sleep(0.1 * count)
    if html is None or len(html) == 0:
        return None

    #解析json数据
    info = json.loads(html)
    day = ''
    result = {}
    try:
        if info.has_key('title') and info.has_key('f_pgmtime') and info.has_key('video'):
            day = info.get('f_pgmtime').split(' ')[0]
            result['day'] = day
            result['title'] = info.get('title')
            result['vid'] = vid
            video = info.get('video')
            cKey = 'chapters'
            if video.has_key('validChapterNum'):
                cNum = int(video.get('validChapterNum'))
                if cNum > 1:
                    cKey += '2'
            if video.has_key(cKey):
                videos = []
                #warning: 视频可能是多个片段剪辑的
                chapters = video.get(cKey)
                if chapters is not None and len(chapters) > 0:
                    for i in range(0, len(chapters)):
                        chapter = chapters[i]
                        if i == 0:
                            result['image'] = chapter['image']
                        item = {'duration': chapter.get('duration'), 'url': chapter.get('url')}
                        videos.append(item)
                result['videos'] = videos
    except:
        result = None
    return result

def getStoreFilePrefixName(vInfo):
    '''
    拼接存储文件和图片的前缀
    :param vInfo: 视频信息map
    :return:
    '''
    if vInfo is None:
        return None
    #日期_id_名称
    list = []
    list.append(vInfo['day'])
    list.append(vInfo['vid'])
    list.append(vInfo['title'])
    return '_'.join(list)

def downloadImage(cid, vInfo):
    '''
    下载图片
    :param cid: 分类Id
    :param vInfo: 视频信息
    :return: success?
    '''
    basedir = configCache.get('base_store')
    ciddir = basedir + '/' + cid
    videodir = ciddir + '/videos'
    filepath = videodir + '/' + getStoreFilePrefixName(vInfo) + '.jpg'
    return readAndSaveFile(vInfo['image'], filepath)

def downloadVideo(cid, partNum, vInfo):
    '''
    下载视频
    :param cid: 分类Id
    :param vInfo: 视频信息
    :return: success?
    '''
    basedir = configCache.get('base_store')
    ciddir = basedir + '/' + cid
    videodir = ciddir + '/videos'
    filepath = videodir + '/' + getStoreFilePrefixName(vInfo) + '_' + str(partNum) + '.mp4'
    return readAndSaveFile(vInfo['url'], filepath)


def doCategorySiper(cid, maxpage):

    for page in range(1, maxpage + 1):
        vList = getVideoIdList(cid, page)
        if vList is not None and len(vList) > 0:
            for vid in vList:
                #判断文件是否已经处理完成，如果处理完成就跳过
                if Tools.watchdog.hasFinished(cid, vid, True):
                    continue
                else:
                    #解析单个视频信息
                    vInfo = getVideoInfo(vid)
                    #下载图片和视频文件
                    if vInfo is not None and vInfo.has_key('videos'):
                        prefixName = getStoreFilePrefixName(vInfo)
                        storeImage = downloadImage(cid, vInfo)
                        videos = vInfo['videos']
                        storeVideo = True
                        for i in range(0, len(videos)):
                            item = videos[i]
                            item['day'] = vInfo['day']
                            item['vid'] = vInfo['vid']
                            item['title'] = vInfo['title']
                            if downloadVideo(cid, i + 1, item):
                                #写单个视频文件下载完成的标记文件
                                Tools.watchdog.writeFinished(cid, vInfo, False, i + 1)
                            else:
                                storeVideo = False
                        if storeImage and storeVideo:
                            #写整个视频栏目下载完成的标记文件
                            Tools.watchdog.writeFinished(cid, vInfo, True)
                            print 'Success : %s' % prefixName
                        else:
                            print 'Fail : %s' % prefixName
                #设置间隔时间，避免给对方服务器造成压力
                time.sleep(0.1)
        print '[Done] cid=%s, page=%d' % (cid, page)

    print '[Done] process job done, cid=%s' % cid
