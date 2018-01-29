import pymysql
import sqlite3
import redis
import os
BASE_DIR = os.path.dirname(__file__)
try:
	# conn = pymysql.connect(host='*',
	#                        port=3306,
	#                        db='*',
	#                        user='*',
	#                        password='*')
	conn = sqlite3.connect(os.path.join(BASE_DIR,"BingoProxy.db"),check_same_thread = False)
	                       
except:
	print("sql connect error")
	exit(0)

try:
	r = redis.Redis(host='127.0.0.1',
	                password='')
except:
	print("redis connect error")
	exit()

# monitor_type=['all','matching','no','content-type'] 监听url的类型
monitor_type='no'
monitor_url=[u'http://www.baidu.com','reg:http(.+)']
filter_type=['text/html']

#---------------init-------
if not r.exists("monitor_type"):
	r.set("monitor_type","no")
for i in monitor_url:
	r.sadd("monitor_url",i)
for i in filter_type:
	r.sadd("filter_type",i)

#日志模块

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='bingoproxy.log',
                filemode='w')
import json

#指定监听那些文件类型
f=open(os.path.join(BASE_DIR,"alltype.json"),'r').read()
all_type=json.loads(f)