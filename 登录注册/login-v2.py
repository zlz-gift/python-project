# 1. 运行之后有菜单，可以选择登录还是注册
# 2. 将用户名和密码存在字典中，{"张三": {"password":"123456", "count":"3"}}
# 3. 密码错误3次，程序自动退出
# 4. 将db保存到db文件中，每一行一个用户 张三👌123456🌸3
while 1:
    with open("db","a+",encoding="utf_8") as f:
        f.seek(0)
        data = f.readlines()
    
    db={}
    if len(data) > 0:
        for line in data:
            temp1 = line.strip().split("👌")
            temp2 = temp1[1].split("🌸")
            db[temp1[0]] = {
                "password" : temp2[0],
                "count":temp2[1]
            }
    print("menu".center(30, "="))
    print("1. login".center(30, " "))
    print("2. register".center(30, " "))
    print("3. exit".center(30, " "))
    choice = input("请选择:")
    if choice == "1":
        # 登录的逻辑
        username = input("输入用户名：")
        if username in db:
            count = int(db[username]["count"])
        else:
            print("用户名不存在")
            continue

        password = input("输入密码：")
        # 判断剩余密码尝试次数
        if  count > 0:
            if db[username]["password"] == password:
                print("登录成功！")
                db[username]["count"] = 3
            else:
                print("用户名或密码错误！")
                db[username]["count"] = count - 1
        else:
            print("账户已被封禁！")
    elif choice == "2":
        # 注册的逻辑
        username = input("输入用户名：")
        # 判断用户是否已存在
        if username in db:
            print("用户名已存在")
            continue
        password = input("输入密码：")
        # 添加用户名到字典中，值是密码和剩下尝试的次数
        db[username] = {
            "password": password,
            "count": 3
        }
    elif choice == "3":
        # 退出
        print("再见！")
        break

    with open("db","w",encoding="utf-8") as f:
        for key,value in db.items():
            line = f"{key}👌{value['password']}🌸{value['count']}\n"
            f.write(line)