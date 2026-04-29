import socket 
import json
import time
import hashlib

def put_db():
    with open("db", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def get_db():
    with open("db", "a+", encoding="utf-8") as f:
        f.seek(0)
        if len(f.read()) == 0:
            print("数据库初始化成功！")
            db = {}
        else:
            f.seek(0)
            db = json.load(f)
    return db

def check_user(username):
    if username in db:
        return True
    else:
        return False
    
def register(username, password, email):
    now_time = time.time()
    password = password + "xlsyyds666(*^▽^*)" + str(now_time)
    password = hashlib.sha256(password.encode()).hexdigest()
    db[username] = {
        "password": password,
        "count": 3,
        "email": email,
        "r_time": time.time()
    }

def login(username, password):
    count = int(db[username]["count"])
    if count > 0:
        r_time = db[username]["r_time"]
        password = password + "xlsyyds666(*^▽^*)" + str(r_time)
        password = hashlib.sha256(password.encode()).hexdigest()
        if db[username]["password"] == password:
            db[username]["count"] = 3
            login_user.append(username)
            return 1
        else:
            db[username]["count"] = count - 1
            return 2
    else:
        return 3
    
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(('0.0.0.0', 8080))
sk.listen()
login_user = []
conn, addr = sk.accept()
while True:
    msg = json.loads(conn.recv(4096).decode("utf-8"))
    db = get_db()
    print(msg)

    if msg.get("option") == "check_user":
        if check_user (msg["username"]):
            data = {"status": "ok", "code": 1}
        else:
            data = {"status": "ok", "code": 0}
        conn.send(json.dumps(data).encode("utf-8"))

    if msg.get("option") == "login":
        username = msg["username"]
        password = msg["password"]
        login_code = login(username,password)
        if login_code == 1:
            conn.send(json.dumps({"status": "ok", "code": 1}).encode("utf-8"))
        elif login_code == 2:
            conn.send(json.dumps({"status": "ok", "code": 0, "info": "密码错误"}).encode("utf-8"))
        elif login_code == 3:
            conn.send(json.dumps({"status": "ok", "code": 0, "info": "账户已封禁"}).encode("utf-8"))
    put_db()
