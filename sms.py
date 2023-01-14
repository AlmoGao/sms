import db
from flask import g
from ronglian_sms_sdk import SmsSDK
import json

# 发送短信
def send(tid, mobile, datas):
    db.get_db()
    result = db.query_db('select rowid, * from smsconfig', '', True)
    db.close_db()
    print(result)
    if result is None:
        return
    sdk = SmsSDK(result['accountSid'], result['token'], result['appid'])
    # tid = '1'
    # mobile = '18080575570'
    # datas = ('3579d', '20')
    resp = sdk.sendMessage(tid, mobile, datas)
    return resp

# 存入记录
def saveHis(username, createTime, sendTime, mobile, tid, content, datas, status, result):
    db.get_db()
    try:
        g.db.execute("INSERT INTO smshistory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(username), str(createTime), str(sendTime), str(mobile), int(tid), str(content), str(datas), int(status), str(result)))
        g.db.commit()
        print('插入发送记录数据成功')
        db.close_db()
        return True
    except:
        g.db.rollback()
        print('插入发送记录数据失败')
        db.close_db()
        return False


# 撤销未发送的短信
def deletePresend(rowid):
    db.get_db()
    try:
        g.db.execute("DELETE FROM smshistory WHERE rowid = ?", (rowid,))
        g.db.commit()
        print('删除成功')
        db.close_db()
        return True
    except:
        g.db.rollback()
        print('删除失败')
        db.close_db()
        return False


# 查询所有发送记录
def allHistory():
    result = db.query_db('select rowid, * from smshistory')
    return json.dumps(result) 

# 查询所有未发送记录
def allPresend():
    result = db.query_db('select rowid, * from smshistory where status = 9')
    return json.dumps(result)  
