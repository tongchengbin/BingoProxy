import sys
import json
import re
import traceback
import base64
from mitmproxy import http, ctx, websocket
import sqlite3
import pymysql
# conn=sqlite3.connect("data.db")
# c=conn.cursor()
conn = pymysql.connect(host='106.14.121.43', user='root',
                       password='abc123456', db='data', charset="utf8")
c = conn.cursor()
sql = "select answer from questions where quiz='{}'"
import json
import redis
import os
r = redis.Redis(host='127.0.0.1', port=6379, password='tongchengbin')
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='midking.log',
                    filemode='a')


def question(quiz, school, _type, options):
    sql = "insert into questions(quiz,school,type,options) VALUES('{quiz}','{school}','{_type}','{options}','{answer}')".format(
        quiz=quiz, school=school, _type=_type, options=options)
    try:
        c.execute(sql)
        conn.commit()
    except Exceptions as e:
        logging.DEBUG(e)


def response(flow: http.HTTPFlow) -> None:
    data = flow.get_state()
    print(data)
    if "findQuiz" in data['request']['path'].decode('utf-8'):
        # 获取题目信息
        data_find = data['response']['content'].decode('utf-8')
        find_json = json.loads(data_find)
        quiz = find_json['data']['quiz']
        options = find_json['data']['options']
        school = find_json['data']['school']
        _type = find_json['data']['type']
        body = data['request']['content'].decode('utf-8')
        roomid = body.split("&")[0].split("=")[1]
        quizNum = body.split("&")[1].split("=")[1]
        # 存储题目信息 后面更新或者存储
        upsql = "insert into questions(quiz, school, type, options, answer)\
            VALUES('{quiz}', '{school}', '{_type}', '{options}', '{answer}')".format(
                quiz=quiz,
                school=school,
                _type=_type,
                options=str(options).replace("'","\\'"),
                answer='')
        try:
            c.execute(upsql)
            conn.commit()
            print("题目存储成功")
        except pymysql.err.IntegrityError:
            pass
        except Exception as e:
            print(upsql)
            print("信息存储失败",e)
        r.set('roomid', roomid)
        r.set('quizNum', quizNum)
        r.set('quiz',quiz)
        r.set('options',options)
        c.execute(sql.format(quiz))
        answer = c.fetchone()[0]
        #获取答案的index  用于自动答题
        if answer:
            answerOK=1
            for op in options:
                if op==answer:
                    break
            answerOK+=1
            r.set("answerOK",answerOK)
            print("答案是：",answer)
            newresp = data['response']['content'].decode('utf-8').replace(answer, answer+"----")
            flow.response.content = newresp.encode('utf-8')
            print("请注意-----")
        else:
            r.set("answerOK",1)
            answer = ''
            print("没有匹配到题目")
    if "choose" in data['request']['path'].decode('utf-8'):
        #---------------------------------------------------自动修改答案开关
        request_body=data['request']['content'].decode('utf-8')
        city_option=re.search('option=',request_body).end()
        answerOK=r.get('answerOK').decode('utf-8')
        new_request_body=request_body[:city_option]+answerOK+request_body[city_option+1:]
        #修改请求数据
        print("请求数据：",new_request_body)
        flow.request.content=new_request_body.encode('utf-8')
        #-----------------------------------------------------------------自动答题开关

        data_choose = data['response']['content'].decode('utf-8')
        

        resp_choose_json = json.loads(data_choose)
        
        # 1234 option 序号1-  正确答案
        answer = resp_choose_json['data']['answer']
        roomid = r.get('roomid').decode('utf-8')
        quizNum = r.get('quizNum').decode('utf-8')
        print(roomid == data['request']['content'].decode('utf-8').split("&")[0].split("=")[1])
        print(quizNum == data['request']['content'].decode('utf-8').split("&")[1].split("=")[1])
        print(data['request']['content'].decode('utf-8').split("&")[1].split("=")[1] == 1)
        if roomid == data['request']['content'].decode('utf-8').split("&")[0].split("=")[1] and (quizNum == data['request']['content'].decode('utf-8').split("&")[1].split("=")[1] or data['request']['content'].decode('utf-8').split("&")[1].split("=")[1] == 1 ):
            # if data_choose_json['response']['data']['yes'] == 'false':
            # 答案错误 更新答案
            #全部更新
            quiz=r.get('quiz').decode('utf-8')
            options_str=r.get('options').decode('utf-8')
            print(options_str)
            options=eval(options_str)#列表
            answer=options[answer-1]
            print("正确答案：",answer)
            update_answer_sql="update questions set answer='{answer}' where quiz='{quiz}'".format(quiz=quiz,answer=answer)
            print(update_answer_sql)
            try:
                c.execute(update_answer_sql)
                conn.commit()
                print("答案更新成功")
            except Exception as e:
                print("update_answer_sql ERROR:"+e)
        else:
            print(resp_choose_json)
            print(r.get('quiz').decode('utf-8'))
            print("原先的：",roomid,quizNum)
            print("第二次：",data['request']['content'].decode('utf-8').split("&")[0].split("=")[1],data['request']['content'].decode('utf-8').split("&")[1].split("=")[1])
            print("答案和题号不对",answer)
            print("本次答案对应的题目是",r.get('quiz').decode('utf-8'))
