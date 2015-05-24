####################################################
NOTE: python lib 2.6上正常运行，其他版本未测试过
Author: wangqiang
####################################################
开发纪要
查找分类信息的入口页面
http://tv.cntv.cn/videoset/C10190

步骤分析：
1、分页获取视频信息（图文信息和视频编号ID）
setid=分类
http://tv.cntv.cn/index.php?action=videoset-videolistbytype&class=lanmu&setid=C10190&istiyu=0&page=1
2、获取视频资源下载信息
pid=资源id（上一步返回的源码中可以找到）
http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=b76d9f90b9643ddf588d37a30a4e5c44&modifyed=false

###########################################
使用前，需要先设置CONF中的配置
category.ini 主要记录分类ID和中文名称的对应关系 ID需要人工在站点上检出（可以通过http://tv.cntv.cn/videoset/search?type=CN02这个入口查到）
common.ini 主要是[task]这个section的设置
    base_store： 指定一个本机磁盘路径就可以，确保当前用户有写权限（如不指定或者指定的路径不存在，下载的资源会保存到当前路径的"STORE"目录）
    spider_cate:  指定需要抓取的分类ID，分类ID来源同category.ini
    max_page:  指定需要抓取的分类最大页数，设置的值越大，耗时会越长
    NOTE: spider_cate不建议设置太多，过多对机器资源消耗较大且有封IP的风险
          max_page也不建议设置过长
**可以在多台机器上设置不同的参数，并行抓取

############################################
存储路径下的文件和文件夹说明
1、每个分类会以分类ID存储一个文件
2、每个分类文件夹下会有 finished logs videos三个子文件夹
    finished: 记录任务完成的情况，主要是程序执行和任务追踪用到（非特殊情况，不要清理这个路径的文件）
    logs: 日志文件路径，目前未用到
    videos: 保存下载的视频资源和截图文件(the things you want)
3、videos下文件命名规则
    图片文件： 2015-05-24_4ae0fca5a3bd4e65a9ec8fbc172b8fc0_[朝闻天下]习近平出席中日友好交流大会并发表重要讲话.jpg
              以下划线分隔： 日期_视频ID_视频标题.jpg
    视频文件： 2015-05-24_4ae0fca5a3bd4e65a9ec8fbc172b8fc0_[朝闻天下]习近平出席中日友好交流大会并发表重要讲话_1.mp4
              以下划线分隔： 日期_视频ID_视频标题_剪辑编号.mp4  (像朝闻天下这样的长时间栏目，通常是有多个视频剪辑合的)

##############################################
关于脚本的启动
首先需要确保机器上有python运行环境，最好是2.6版本（用习惯了这个版本^_^）
命令行在脚本路径下，执行  python spiderCurrent.py

可以通过设置windows定时任务或者linux的crontab来调用执行
建议按照栏目自身更新频率（比如有些是周更新，有些是日更新的），设置多个不同的任务