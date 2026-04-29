import flask
import json
import loginv6

app = flask.Flask(__name__)

@app.route('/login',methods=['POST','GET']) # type: ignore
def login():
    if flask.request.method == "GET":
        with open('html/login.html','r',encoding='utf-8') as f:
            data = f.read()
        return data
    elif flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        if not loginv6.check_user(username):
            return "用户名不存在"
        login_ret = loginv6.login(username, password)
        if login_ret == 1:
             return "登录成功"
        elif login_ret == 2:
            return "密码错误"
        else:
            return "账号封禁"

app.run(host='0.0.0.0', port=5000, debug=True)