import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from flask import Flask, request, Response, jsonify, render_template, g, redirect
import config
import json

import datetime


class DateEncoder(json.JSONEncoder):
    '''json dumps 无法转换datetime 所以重新了json模块'''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif obj:
            print(obj)
            return obj
        else:
            return json.JSONEncoder.default(self, obj)



app = Flask(__name__)
app.config['DEBUG'] = True
app.debug = True
dbconn=config.conn
dbc=dbconn.cursor()

@app.route('/',methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method=="GET":
        records_sql='SELECT * FROM agency limit 50;'
        try:
            dbc.execute(records_sql)
            records=dbc.fetchall()
        except Exception as e:
            print(e)
            records=[]
        print(records)
        return render_template('index.html',records=records,)
    else:
        post_form=request.form
        action=post_form.get('action')
        if action == 'get_record':
            record_id=post_form['obj']
            sql = 'SELECT * FROM agency WHERE id=%s' % (record_id)
            try:
                dbc.execute(sql)
                record = dbc.fetchone()
            except Exception as e:
                print(e)
                record = ''
           #计算排序
            data={}
            data['id']=record[0]
            data['url'] = record[1]
            data['method'] = record[2]
            data['status_code']=record[3]
            data['host'] = record[4]
            data['path'] = record[5]
            data['content_type'] = record[6]
            data['request_headers'] = record[7]
            data['response_headers'] = record[8].replace('""','"')
            data['request_content'] = record[9]
            data['response_content'] = record[10]
            data['recordtime'] = record[11]
            respdata={'status':True,"data":data}
            print(json.dumps(data['response_headers'],cls=DateEncoder))
            return Response(json.dumps(respdata,cls=DateEncoder))
        elif action == "delrecord":
            obj=request.form['obj']
            sql="delete from %s where id=%s"%("agency",obj)
            try:
                dbc.execute(sql)
                dbconn.commit()
                data={"status":True}
            except Exception as e:
                print(e)
                data={"status":False}
            return Response(json.dumps(data))
        else:
            data = {'status': False, "data": ''}
            return Response(json.dumps(data))

@app.route('/settings',methods=['GET', 'POST'])
def settings():
    if request.method=="POST":
        action=request.form['action']
        data={"status":True}
        if action=='addtype':
            obj=request.form['obj']
            config.r.sadd("filter_type",obj)
        elif action=='deltype':
            obj=request.form['obj']
            config.r.srem("filter_type",obj)
        elif action == "changemonitor":
            obj = request.form['obj']
            config.r.set("monitor_type",obj)
        elif action=="addurl":
            obj = request.form['obj']
            config.r.sadd("monitor_url",obj)
        elif action=="delurl":
            obj = request.form['obj']
            config.r.srem("monitor_url",obj)
        return Response(json.dumps(data))
    alltype=[x.decode("utf-8") for x in config.r.smembers("filter_type")]
    monitor_url=[x.decode("utf-8") for x in config.r.smembers("monitor_url")]
    monitor_type=config.r.get("monitor_type").decode("utf-8")
    return render_template('settings.html',alltype=alltype,monitor_url=monitor_url,monitor_type=monitor_type)
if __name__ == '__main__':
    app.run(port=5004)
