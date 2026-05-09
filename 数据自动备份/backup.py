# 1. 周期性的将指定目录压缩到backup文件夹
# 2. 使用年月日时分秒.zip作为备份文件名
# 3. 需要能够记录每次备份的日志，日志中需要有备份文件名，备份完成的时间，备份文件的md5
# 4. 需要判断最新的备份是否和上一份一样，如果一样就删除掉新的备份

import shutil
import os
import time
import hashlib
import json

src_dir = "note"
backup_dir = "backup"

if  not os.path.isdir(src_dir):
    raise FileNotFoundError(f"需要备份的文件夹'{src_dir}'不存在！")

if not os.path.isdir(backup_dir):
    os.mkdir(backup_dir)

while True:
    time.sleep(3)
    str_time = time.strftime("%Y%m%d-%H%M%S")
    ret = shutil.make_archive(f'{backup_dir}{os.sep}{str_time}','zip',src_dir)
    with open(f"{backup_dir}{os.sep}{str_time}.zip", "rb") as f:
        backup_info = {
            "filename": str_time + ".zip",
            "timestamp": time.strftime("%Y%m%d-%H%M%S"),
            "md5": hashlib.md5(f.read()).hexdigest()
        }
        with open(f"{backup_dir}{os.sep}backup_info.json", "a+") as f:
            f.seek(0)
            data = f.read()
            old_backup_info = {"md5": "none"}
            if len(data) != 0:
                old_backup_info = json.loads(data)
            if old_backup_info["md5"] == backup_info["md5"]:
                os.remove(f"{backup_dir}{os.sep}{str_time}.zip")
                print(f"备份失败：文件未发生变化！")
                continue
    with open(f"{backup_dir}{os.sep}backup_info.json", "w") as f:
        json.dump(backup_info, f, indent=4, ensure_ascii=False)
    print(f"备份成功：{ret}")