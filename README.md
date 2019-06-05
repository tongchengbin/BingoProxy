# 开始
git clone https://github.com/tongchengbin/BingoProxy.git
# 设置
  填写数据库信息 redis
# 开始使用
## 启动
mitmdump -s BingoProxy.py
![http://ozelrebbz.bkt.clouddn.com/2f578bdee356acfe765c09bc92b54108.png](http://ozelrebbz.bkt.clouddn.com/2f578bdee356acfe765c09bc92b54108.png)
## 设置代理
  windows
  这里以360浏览器为例
![](http://ozelrebbz.bkt.clouddn.com/ac760cd5e76a08f3ab75442190d562ad.png)
## 安装证书
访问mitm.it
出现如下界面 代理设置正确
![](http://ozelrebbz.bkt.clouddn.com/d922840854af2687be2d86c0ddfc9c36.png)
出现如下界面  代理设置错误
![](http://ozelrebbz.bkt.clouddn.com/9cc3ffafc3f0ef0c793ceac7a2c97bf5.png)
选择相应设备的证书 安装至根目录
# web控制器
web控制器是基于flask编写的 目前只实现了简单的功能 后期会慢慢改善
运行webcontrol.py 打开web控制器127.0.0.1:5004
![](http://ozelrebbz.bkt.clouddn.com/e95960552f7f3fa0654731f4a71263d8.png)
## 监听方式
### 全监听方式
    即监听所有请求
### 根据请求url进行匹配 可以指定具体的URL 同时支持正则表达式
### 根据文件类型监听 例如.html文件 text/html
### 停止监听
![](http://ozelrebbz.bkt.clouddn.com/db4ba0f77fd3b568683f4395b468537e.png)
]
