# 模板
import db
import json
from flask import g

# 修改一条模板
def updateTemplate(tid, content, params):
    try:
        g.db.execute("UPDATE smstemplate SET content=?,params=?  WHERE id = ?", (content, params, tid))
        g.db.commit()
        print('修改模板数据成功')
        return True
    except:
        g.db.rollback()
        print('修改模板数据失败')
        return False

# 删除一条模板
def delTemplate(tid):
    try:
        g.db.execute("DELETE FROM smstemplate WHERE id = ?", (tid,))
        g.db.commit()
        print('删除模板数据成功')
        return True
    except:
        g.db.rollback()
        print('删除模板数据失败')
        return False

# 增加一条模板
def addTemplate(tid, content, params):
    result = db.query_db('select rowid, * from smstemplate where id=?', (tid,))
    if len(result) > 0:
        return False
    try:
        g.db.execute("INSERT INTO smstemplate VALUES (?, ?, ?)", (tid, content, params))
        g.db.commit()
        print('插入模板数据成功')
        return True
    except:
        g.db.rollback()
        print('插入模板数据失败')
        return False    

# 查询所有模板
def allTemplate():
    result = db.query_db('select rowid, * from smstemplate')
    return json.dumps(result)