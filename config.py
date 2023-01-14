# 配置
import db
import json
from flask import g

# 修改配置
def updateConfig(rowid,appid,accountSid,token,restUrl):
    try:
        g.db.execute("UPDATE smsconfig SET appid=?,accountSid=?,token=?,restUrl=?  WHERE rowid = ?", (str(appid),str(accountSid),str(token),str(restUrl),rowid))
        g.db.commit()
        print('修改成功')
        return True
    except:
        g.db.rollback()
        print('修改失败')
        return False

# 查询配置
def allConfig():
    result = db.query_db('select rowid, * from smsconfig')
    return json.dumps(result[0])