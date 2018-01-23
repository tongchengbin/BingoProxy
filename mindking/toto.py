import sqlite3
import pymysql
p = pymysql.connect(host='', user='',
                    password='', db='',charset="utf8")
cp = p.cursor()
s = sqlite3.connect('data.db')
cs = s.cursor()
getsql = "select * from questions"



cs.execute(getsql)
data = cs.fetchall()
for q in data:
    quiz = q[0]
    school = q[1]
    _type = q[2]
    options = q[3]
    answer = q[4]
    upsql = "insert into questions(quiz,school,type,options,answer) VALUES('{quiz}','{school}','{_type}','{options}','{answer}')".format(
        quiz=quiz,
        school=school, 
        _type=_type, 
        options=options,
        answer=answer)
    try:
    	cp.execute(upsql)
    	p.commit()
    except pymysql.err.IntegrityError:
    	pass
    except Exception as e:
    	print(e)
