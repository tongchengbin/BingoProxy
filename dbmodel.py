from config import conn, logging
from pymysql.err import InternalError
c = conn.cursor()


def init_table():
    '''
     创建数据表
    '''
    create_table_sql = '''
    create table agency(
        id INT  AUTO_INCREMENT primary key,
        url varchar(255),
        method varchar(20),
        status_code smallint,
        host varchar(255),
        path varchar(255),
        content_type varchar(128),
        request_headers text,
        response_headers text,
        request_content text null,
        response_content text,
        recodetime datetime DEFAULT NOW()
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''
    try:
        c.execute(create_table_sql)
        conn.commit()
    except InternalError:
        pass
    except Exception as e:
        logging.warning('数据库创建失败')
        print("创建数据库失败:", e)


init_table()


def insert_agency(
        url,
        method,
        status_code,
        host,
        path,
        content_type,
        request_headers,
        response_headers,
        request_content,
        response_content
):
    sql = '''INSERT INTO agency(url,method,status_code,host,path,\
        content_type,\
        request_headers,\
        response_headers,\
        request_content,\
        response_content\
        )VALUES(
        '{url}','{method}',{status_code},'{host}','{path}',\
        '{content_type}',\
        '{request_headers}',\
        '{response_headers}',\
        '{request_content}',\
        '{response_content}')'''.format(
        url=url,
        method=method,
        status_code=status_code,
        host=host,
        path=path,
        content_type=content_type,
        request_headers=request_headers,
        response_headers=response_headers,
        request_content=request_content,
        response_content=response_content
    )
    try:
        # print(sql)
        c.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        logging.warning("save data error SQL:", sql)
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print(sql)
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        return e
