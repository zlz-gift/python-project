# 1. 运行之后有菜单，可以选择登录还是注册
# 2. 将用户名和密码存在字典中，{"张三": {"password":"123456", "count":"3"}}
# 3. 密码错误3次，程序自动退出
db = {}
while 1:
    print("menu".center(30,'='))
    print("1. login".center(30, " "))
    print("2. register".center(30, " "))
    print("3. exit".center(30, " "))
    choice = input("请选择：")
    if choice == "1":
        username = input("请输入用户名:")
        password = input("请输入密码:")
        if username not in db:
            print("用户不存在")
        elif db[username]["count"] > 0:
            if db[username]['password'] == password:
                print("登录成功！")
                db[username]['count'] = 3
            else:
                print("用户名或密码错误！")
                db[username]["count"] -=1
        else:
            print("用户已被封禁！")
    elif choice == "2":
        username = input("输入用户名：")
        if username in db:
            print("用户已存在！")
            continue
        password = input("输入密码：")
        db[username] = {
            "password":password,
            "count":3
        }
    elif choice == "3":
        print("再见！")
        break               
