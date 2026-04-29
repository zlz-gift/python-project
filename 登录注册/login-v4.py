# 1. 运行之后有菜单，可以选择登录还是注册
# 2. 将用户名和密码存在字典中，{"张三": {"password":"123456", "count":"3"}}
# 3. 密码错误3次，程序自动退出
# 4. 将db保存到db文件中，每一行一个用户 张三👌123456🌸3
# 5. 使用函数将代码解耦
# 6. 菜单增加两个个选项，3. 玩游戏   4. 退出登录
## 6.1 选择3，会判断是否登录，如果没登录提示请登录，如果已经登录，显示欢迎{玩家名}和一个网址https://arcxingye.github.io/rr/?utm_source=xinquji
## 6.2 选择4，会清除登录状态
# 7.控制日志的开关
import time
flag = True

def run_log(flag):
    def outer(func):
        # 可以在日志中记录什么时候，什么函数开始和结束
        def inner(*args, **kwargs):
            func_name = func.__name__
            if flag: 
                open("run.log", "a", encoding="utf-8").write(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')}-{func_name}-开始运行\n")
            res = func(*args, **kwargs)
            if flag:
                open("run.log", "a", encoding="utf-8").write(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')}-{func_name}-结束运行\n")
            return res
        return inner
    return outer

def auth(func):
    def inner(*args,**kwargs):
        if len(login_user)>0:
            res = func(*args,**kwargs)
            return res
        else:
            print("请登录")
            return False
    return inner

@run_log(True)
def login(username, password):
    # 登录的功能, 返回1表示登录成功， 2表示密码错误， 3表示账号封禁
    count = int(db[username]["count"])
    if count > 0:
        if db[username]["password"] == password:
            db[username]["count"] = 3
            # 登录成功后，将当前用户名加入已经登录的列表中
            login_user.append(username)
            return 1
        else:
            db[username]["count"] = count - 1
            return 2
    else:
        return 3

@run_log(True)
def register(username, password):
    # 注册的功能
    # 添加用户名到字典中，值是密码和剩下尝试的次数
    db[username] = {
        "password": password,
        "count": 3
    }

@run_log(True)
def get_db():
    # 读取数据库文件
    with open("db", "a+", encoding="utf-8") as f:
        f.seek(0)
        data = f.readlines()

    if len(data) > 0:
        for line in data:
            # 张三👌123456🌸3\n
            temp1 = line.strip().split("👌")
            # ["张三","123456🌸3"]
            temp2 = temp1[1].split("🌸")
            db[temp1[0]] = {
                "password": temp2[0],
                "count": temp2[1]
            }

@run_log(True)
def put_db():
    # 写入数据库文件
    with open("db", "w", encoding="utf-8") as f:
        for key, value in db.items():
            line = f"{key}👌{value['password']}🌸{value['count']}\n"
            f.write(line)

def check_user(username):
    # 判断用户名是否存在
    if username in db:
        return True
    else:
        return False

@auth
@run_log(True)
def play_game():
    print(f"欢迎玩家{login_user[-1]}!\n点击开玩：https://arcxingye.github.io/rr/?utm_source=xinquji")

@run_log(True)
def logout():
    login_user.clear()
    print("注销登录成功")


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
        username = input("输入用户名：")
        if not check_user(username):
            print("用户名不存在")
            return
        password = input("输入密码：")
        # 获取到登录函数的结果，而不是每次判断都执行一遍
        login_ret = login(username, password)
        if login_ret == 1:
            print("登录成功")
        elif login_ret == 2:
            print("密码错误")
        else:
            print("账号封禁")
    if num == "2":
        username = input("输入用户名：")
        if check_user(username):
            print("用户名已存在")
        else:
            password = input("输入密码：")
            register(username, password)
    if num == "3":
        play_game()
    if num == "4":
        logout()
    if num == "5":
        return True


# 保存已经登录玩家的名字
login_user = []
while True:
    db = {}
    get_db()
    # print(db)
    if menu():
        break
    put_db()