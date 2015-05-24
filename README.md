抓取cntv资源的工具
入口页面
http://tv.cntv.cn/videoset/C10190

步骤概要：
1、分页获取视频信息（图文信息和视频编号ID）
setid=分类
http://tv.cntv.cn/index.php?action=videoset-videolistbytype&class=lanmu&setid=C10190&istiyu=0&page=1
2、获取视频资源下载信息
pid=资源id（上一步返回的源码中可以找到）
http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=b76d9f90b9643ddf588d37a30a4e5c44&modifyed=false

