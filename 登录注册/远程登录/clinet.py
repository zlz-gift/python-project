# 登录/注册 需要两次校验
## 1.第一次判断用户名是否存在
###  a. 发送请求内容，{"options": "check_user", "username": "张三"}
###  b. 接收请求内容，{"status": "ok", "code": 1}  code: 1表示存在，0表示不存在
## 2. 登录/注册
#### a. 发送的请求内容 {"options": "login/register", "username": "张三", "password": "123123"}
###  b. 接受请求内容，{"status": "ok", "code": 1}  code: 1表示成功，0表示不成功

import socket
import json

sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.connect(("127.0.0.1",8080))

def menu():
    # 打印菜单
    print("=" * 20)
    print('''
    1. 登录
    2. 注册
    3. 玩游戏
    4. 退出登录
    5. 退出
    ''')
    if choice(input("请选择：")):
        return True
    
def choice(num):
    if num == "1":
        username = input("请输入用户名:")
        data = {"option":"check_user","username":username}
        sk.send(json.dumps(data).encode("utf-8"))
        check_result = json.loads(sk.recv(4096).decode("utf-8"))
        if check_result.get("code") == 0:
            print("用户名不存在！")
        else:
            password = input("密码：")
            email= input("邮箱：")
            data = {"options": "register", "username": username, "password": password, "email": email}
            sk.send(json.dumps(data).encode("utf-8"))
            login_result = json.loads(sk.recv(4096).decode("utf-8"))
            if login_result.get("code") == 1:
                print("注册成功！")
            elif login_result.get("code") == 0:
                print(login_result.get("info"))
    if num == "2":
        username = input("用户名：")
        data = {"options": "check_user", "username": username}
        sk.send(json.dumps(data).encode("utf-8"))
        check_result = json.loads(sk.recv(4096).decode("utf-8"))
        if check_result.get("code") == 1:
            print("用户名已存在！")
        elif check_result.get("code") == 0:
            password = input("密码：")
            email = input("邮箱：")
            data = {"options": "register", "username": username, "password": password, "email": email}
            sk.send(json.dumps(data).encode("utf-8"))
            login_result = json.loads(sk.recv(4096).decode("utf-8"))
            if login_result.get("code") == 1:
                print("注册成功！")
            elif login_result.get("code") == 0:
                print(login_result.get("info"))
    
    if num == "3":
        pass
    if num == "4":
        pass
    if num == "5":
        pass

while True:
    menu()


