import os
import json
from flask import Flask, request, g, session, render_template
import db
import sms
import time
import template
import base64
import config
import loop


# code  0-成功  1-失败
# data  0-数据  1-错误提示
def r(code, data):
    return json.dumps({
        "code": code,
        "data": data
    })


# 登录检测
def c():
    if 'username' in session:
        result = db.query_db('SELECT rowid, * FROM smsuser WHERE username=? ', (session['username'],))
        if len(result) == 0:
            return r(401, '登录超时')
        else:
            return False
    else:
        return False

app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'fkdjsafjdkfdl413fadskjfadskljdsfklj'
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# 前端页面
@app.route('/')
def index():
    return render_template('index.html')

# 用户
@app.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    result = db.query_db('SELECT rowid, * FROM smsuser WHERE username=? and password=?', (form['username'], form['password']))
    if len(result) == 0:
        return r(1, '账号或密码错误')
    else:
        token = str(base64.b64encode((form['username'] + str(time.time())).encode('utf-8')), 'utf-8')
        g.db.execute("UPDATE smsuser SET token=? WHERE username=?", (token, form['username']))
        g.db.commit()
        session['username'] = form['username']
        return r(0, {'token': token})
# 更改密码
@app.route('/changPass', methods=['POST'])
def changPass():
    rs = c()
    if rs: return rs  
    form = request.get_json()
    result = db.query_db('SELECT rowid, * FROM smsuser WHERE username=? and password=?', (session['username'], form['password']))
    if len(result) == 0:
        return r(1, '原密码错误')
    else:
        try:
            g.db.execute("UPDATE smsuser SET password=?  WHERE username = ?", (form['newPass'], session['username']))
            g.db.commit()
            print('修改密码成功')
            return r(0, '修改密码成功')
        except:
            g.db.rollback()
            return r(1, '修改密码失败')
        
# 模板
# 查询所有模板
@app.route('/allTemplate', methods=['POST'])
def allTemplate():
    rs = c()
    if rs: return rs
    result = template.allTemplate()
    return r(0, result)
# 新增模板
@app.route('/addTemplate', methods=['POST'])
def addTemplate():
    rs = c()
    if rs: return rs
    form = request.get_json()
    result = template.addTemplate(form['id'], form['content'], form['params'])
    if result is True:
        return r(0, '添加成功')
    else:
        return r(1, '添加失败')
# 修改模板
@app.route('/updateTemplate', methods=['POST'])
def updateTemplate():
    rs = c()
    if rs: return rs
    form = request.get_json()
    result = template.updateTemplate(form['id'], form['content'], form['params'])
    if result is True:
        return r(0, '修改成功')
    else:
        return r(1, '修改失败')
# 删除模板
@app.route('/delTemplate', methods=['POST'])
def delTemplate():
    rs = c()
    if rs: return rs
    form = request.get_json()
    result = template.delTemplate(form['id'])
    if result is True:
        return r(0, '删除成功')
    else:
        return r(1, '删除失败')

# 短信
# 查询所有发送记录
@app.route('/allHistory', methods=['POST'])
def allHistory():
    rs = c()
    if rs: return rs
    result = sms.allHistory()
    return r(0, result)
# 发送短信
@app.route('/send', methods=['POST'])
def send():
    rs = c()
    if rs: return rs  
    form = request.get_json()
    timestamp = str(int(round(time.time() * 1000)))
    # 定时发送
    if 'time' in form:
        # 将定时任务存数据库
        result = sms.saveHis(session['username'], timestamp, form['time'], form['mobile'], form['tid'], form['content'], form['datas'], 9, '')
        if result is True:
            return r(0, '操作成功')
        else:
            return r(1, '操作失败')
    else:
        result = sms.send(form['tid'], form['mobile'], form['datas'])
        status = 0
        if (json.loads(result)['statusCode'] == '000000'):
            status = 1
        sms.saveHis(session['username'], timestamp, timestamp, form['mobile'], form['tid'], form['content'], form['datas'], status, json.dumps(result))
        if (json.loads(result)['statusCode'] == '000000'):
            return r(0, result)
        else:
            return r(1, '发送失败，错误码：' + json.loads(result)['statusCode'])
# 批量发送短信
@app.route('/mutipleSend', methods=['POST'])
def mutipleSend():
    rs = c()
    if rs: return rs  
    form = request.get_json()
    timestamp = str(int(round(time.time() * 1000)))
    # 定时发送
    if 'time' in form:
        print('批量定时发送')
        for item in form['list']:
            result = sms.saveHis(session['username'], timestamp, form['time'], item['mobile'], item['tid'], item['content'], item['datas'], 9, '')
        return r(0, '操作成功')
    else:
        print('批量发送')
        successNum = 0
        errorNum = 0
        for item in form['list']:
            print(item)
            result = sms.send(item['tid'], item['mobile'], item['datas'])
            status = 0
            if (json.loads(result)['statusCode'] == '000000'):
                status = 1
                successNum += 1
            else:
                errorNum += 1
            sms.saveHis(session['username'], timestamp, timestamp, item['mobile'], item['tid'], item['content'], item['datas'], status, json.dumps(result))
        return r(0, '发送成功：' + str(successNum) + '条，发送失败：' + str(errorNum) + '条')
        
# 撤销预发送短信
@app.route('/deletePresend', methods=['POST'])
def deletePresend():
    rs = c()
    if rs: return rs
    form = request.get_json()
    result = sms.deletePresend(form['rowid'])
    if result is True:
        return r(0, '删除成功')
    else:
        return r(1, '删除失败')

# 配置
# 查询配置
@app.route('/allConfig', methods=['POST'])
def allConfig():
    rs = c()
    if rs: return rs
    result = config.allConfig()
    return r(0, result)
# 修改配置
@app.route('/updateConfig', methods=['POST'])
def updateConfig():
    rs = c()
    if rs: return rs
    form = request.get_json()
    result = config.updateConfig(form['rowid'],form['appid'],form['accountSid'],form['token'],form['restUrl'])
    if result is True:
        return r(0, '修改成功')
    else:
        return r(1, '修改失败')

# 创建数据库
db.create_db(app)


# 开启任务循环
loop.start(app)

if __name__ == '__main__':
   app.run()


