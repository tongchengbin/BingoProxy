#save requests response to mysql
from mitmproxy import http, ctx, websocket
from config import conn,r
import config
c=conn.cursor()
import re
import json
import time



from dbmodel import *
#定义需要监听的url  {正则表达式 完整url}
monitor_url=config.monitor_url
def judge_monitor_for_single(url):
    '''
    传入一个url 判断是否需要监听
    '''
    for u in monitor_url:
        if u.startswith("reg:"):
            #正则表达式
            if re.search(u[5:],url):
                return u
        else:
            if u==url:
                return u
    return False
def judge_monitor_for_type(response):
    '''通过文件类型 盘独生女是否需要存储'''
    content_type=response.headers['Content-Type'].split(";")[0]
    print("############################################  content-type:",content_type)
    filter_type=[x.decode("utf-8") for x in config.r.smembers("filter_type")]
    if content_type in filter_type:
        return True
    else:
        return False
def parser_data(request,response):
    #file_path 用于存储响应文件数据
    file_path='responseFile'
    '''传入flow.request flow.response  解析出数据'''
    url = request.host+'/'+ request.path
    method = request.method                      #str
    request_headers=json.dumps({key:val for (key,val) in request.headers.items()})#<class 'mitmproxy.net.http.headers.Headers'>
    try:
        request_content=request.content.decode('utf-8')
    except:
        request_content='不支持预览类型'               #bytes
    status_code=response.status_code  #int
    host=request.host
    path=request.path
    content_type=response.headers['Content-Type']
    response_headers=json.dumps({key:val for (key,val) in response.headers.items()})#<class 'mitmproxy.net.http.headers.Headers'>
    filename=file_path+"/"+str(int(time.time()))+config.all_type.get(content_type,"kn")
    with open(filename,'wb') as f:
        f.write(response.content)
    response_content=filename
    insert_code=insert_agency(
        url,
        method,
        status_code,
        host,
        path,
        content_type,
        request_headers,
        response_headers,
        request_content,
        response_content)
    #开始存储数据
    print("#######################################    Insert code:",insert_code)



def response(flow: http.HTTPFlow) -> None:
    monitor_type=r.get("monitor_type").decode('utf-8')
    data = flow.get_state()
    print("+++++++++++++++++++++++++",monitor_type)
    if monitor_type == 'no':
        pass
    elif monitor_type=="all":
        #监听所有的url 存储
        parser_data(flow.request, flow.response)
    elif monitor_type =='single':
        # 监听指定类型
        url=flow.request.url
        juge_result=judge_monitor_for_single(url)
        if juge_result:
            #juge_result = 匹配条件
            parser_data(flow.request,flow.response)
        else:
            pass
    elif monitor_type=="content-type":
        '''根据文件类型判断'''
        juge_result=judge_monitor_for_type(flow.response)
        if juge_result:
            #juge_result = 匹配条件(文件类型)
            parser_data(flow.request,flow.response)
        else:
            pass
    else:
        pass