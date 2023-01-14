import time
from threading import Timer
import db
from flask import g
import sms
import json

def job(app):
    with app.app_context():
        # 查询未发送的数据
        db.get_db()
        result = db.query_db('select rowid, * from smshistory where status = 9')
        timestamp = int(round(time.time() * 1000))
        for item in result:
            if int(item['sendTime']) <= timestamp:
                print('发送：' + str(item['rowid']))
                # 将数据状态改为发送失败，然后执行发送请求
                try:
                    g.db.execute("UPDATE smshistory SET status=0 WHERE rowid = ?", (item['rowid'],))
                    g.db.commit()
                    print('修改状态成功')
                    # 发送短信
                    rs = sms.send(item['tid'], item['mobile'], item['datas'])
                    status = 0
                    print('发送结果：')
                    print(rs)
                    db.get_db()
                    if (json.loads(rs)['statusCode'] == '000000'):
                        status = 1
                    g.db.execute("UPDATE smshistory SET sendTime=?,status=?,result=? WHERE rowid = ?", (str(timestamp), status, json.dumps(rs), item['rowid']))
                    g.db.commit()
                except:
                    g.db.rollback()
                    print('修改状态失败')
        try:
            db.close_db()
        except:
            print('关闭数据库失败：loop')
        loop_monitor(app)

def loop_monitor(app):
    t = Timer(20, job, (app,))
    t.start()

def start(app):
    with app.app_context():
        loop_monitor(app)