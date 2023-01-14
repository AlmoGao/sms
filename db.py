import sqlite3
from flask import g

DATABASE = 'database.db'

def create_db(app):
    conn = sqlite3.connect(DATABASE)
    print('数据库连接成功')

    # smsuser 表 用户
    # username 账号
    # password 密码
    # type 类型 1-管理员
    # token 登录状态
    # remark 备注
    conn.execute('CREATE TABLE IF NOT EXISTS smsuser (username TEXT, password TEXT, type INTEGER, token TEXT, remark TEXT)')
    
    # smsconfig 表 全局配置
    # appid 短信平台标识
    # accountSid 短信平台Sid
    # token 短信平台token
    # restUrl 请求地址
    conn.execute('CREATE TABLE IF NOT EXISTS smsconfig (appid TEXT, accountSid TEXT, token TEXT, restUrl TEXT)')
    
    # smstemplate 表 模板
    # id 对应平台里已通过的模板id
    # content 模板内容
    # params 参数个数
    conn.execute('CREATE TABLE IF NOT EXISTS smstemplate (id INTEGER, content TEXT, params INTEGER)')

    # smshistory 表 发送记录
    # username 发送人
    # createTime 创建时间
    # sendTime 发送时间
    # mobile 发送号码
    # tid 模板id
    # content 模板内容
    # datas 模板参数
    # status 发送状态 1-成功 0-失败 9-未发送
    # result 发送回执
    conn.execute('CREATE TABLE IF NOT EXISTS smshistory (username TEXT, createTime TEXT, sendTime TEXT, mobile TEXT, tid INTEGER, content TEXT, datas TEXT, status INTEGER, result TEXT )')


    # 插入管理员数据
    cur = conn.execute('select rowid, * from smsuser')
    users = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    if len(users)==0:
        try:
            conn.execute("INSERT INTO smsuser VALUES (?, ?, ?, ?, ?)", ('admin', 'admin123', 1, '', '管理员'))
            conn.commit()
            print('插入管理员数据成功')
        except:
            conn.rollback()
            print('插入管理员数据失败')

    # 插入配置信息
    cur = conn.execute('select rowid, * from smsconfig')
    configs = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    if len(configs)==0:
        try:
            conn.execute("INSERT INTO smsconfig VALUES (?, ?, ?, ?)", ('2c94811c855ce72501858afe50c00452', '2c94811c855ce72501858afe4ff9044b', '87e9276e328b477ba6f19ece6c9662f5', 'https://app.cloopen.com:8883'))
            conn.commit()
            print('插入配置数据成功')
        except:
            conn.rollback()
            print('插入配置数据失败')

    print('数据库创建成功')
    
    conn.close()

    def connect_db():
        return sqlite3.connect(DATABASE)

    @app.before_request
    def before_request():
        g.db = connect_db()

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()
    return

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args) 
    rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def get_db():
    g.db = sqlite3.connect(DATABASE)

def close_db():
    if hasattr(g, 'db'):
        g.db.close()




