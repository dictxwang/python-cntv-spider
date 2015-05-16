#-*- coding: utf8 -*-
__author__ = 'qiangwang'


class CateCache:

    def __init__(self):
        self._map_ = self._readMap_()

    def getMap(self):
        return self._map_

    def convertToName(self, ckey):
        if ckey is None:
            return None
        if self._map_.has_key(ckey):
            return self._map_[ckey]
        else:
            return None

    def _readMap_(self):
        map = {}
        fp = open('CONF/category.ini', 'r')
        for line in fp.readlines():
            if line is None or line == '' or line.startswith('#'):
                continue
            line = line.strip('\n')
            if line.find('=') > 0:
                parts = line.split('=')
                map[parts[0]] = parts[1]
            else:
                map[line] = line
        fp.close()
        print 'read category map done.'
        return map