import flask
import json
import loginv6
import os
app = flask.Flask(__name__)
app.secret_key = "zlz123"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def index():
    return flask.redirect('/login')

@app.route('/login/')
def login():
    with open(os.path.join(BASE_DIR, 'html', 'login.html'), 'r', encoding='utf-8') as f:
        data = f.read()
    return data

@app.route('/register/')
def register():
    with open(os.path.join(BASE_DIR, 'html', 'register.html'), 'r', encoding='utf-8') as f:
        data = f.read()
    return data

@app.route('/user_list/')
def user_list():
    if not flask.session.get('username', None):
        return "<script>alert('请登录！');window.location.href='/login/';</script>"
    with open(os.path.join(BASE_DIR, 'html', 'user_list.html'), 'r', encoding='utf-8') as f:
        data = f.read()
    return data

@app.route('/api/<options>/', methods=['GET', 'POST']) # type: ignore
def api(options):
    """所有对数据的操作,都集中在api中"""
    # 不需要登录就能使用的接口
    if options == "login":
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        login_ret = loginv6.login(username, password)
        if login_ret == 1:
            flask.session['username'] = username
            return json.dumps({"code": 1, "username": username})
        elif login_ret == 2:
            return json.dumps({"code": 0, "msg": "密码错误"})
        else:
            return json.dumps({"code": 0, "msg": "账号封禁"})
    elif options == "register":
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        email = flask.request.form.get('email')
        if loginv6.check_user(username):
            return json.dumps({"code": 0, "msg": "用户名已存在"})
        else:
            loginv6.register(username, password, email)
            return json.dumps({"code": 1, "msg": "注册成功"})
    elif options == "checkuser":
        username = flask.request.args.get('username')
        if not loginv6.check_user(username):
            return json.dumps({"code": 0})
        else:
            return json.dumps({"code": 1})


    # 验证是否登录
    if not flask.session.get('username', None):
        return "<script>alert('请登录！');window.location.href='/login/';</script>"

    # 需要登录之后才能使用
    if options == "reset_user":
        username = flask.request.args.get('username')
        db = loginv6.get_db()
        db[username]["count"] = 3
        loginv6.put_db(db)
        return "<script>alert('解封成功！');window.location.href='/user_list/';</script>"
    elif options == "delete_user":
        username = flask.request.args.get('username')
        db = loginv6.get_db()
        db.pop(username, None)
        loginv6.put_db(db)
        return "<script>alert('删除成功！');window.location.href='/user_list/';</script>"
    elif options == "logout":
        flask.session.clear()
        return "<script>alert('退出成功！');window.location.href='/login/';</script>"
    elif options == "user_list":
        db = loginv6.get_db()
        data = {
            "username": flask.session.get('username'),
            "userlist": db
        }
        return json.dumps(data)


app.run(host='0.0.0.0', port=5000, debug=True)