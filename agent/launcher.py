# -*- coding: utf-8 -*-
"""小助手一键启动脚本：同时启动 web 服务 + cpolar 隧道，并自动抓取公网地址。

用法：双击「一键启动.bat」，或在本目录下运行 .venv 的 python 执行本脚本。
退出：在窗口里按 Ctrl+C，会自动关闭 web 服务和 cpolar 隧道。
"""
import os
import re
import socket
import subprocess
import sys
import threading
import time

# 让输出逐行刷新，重定向/管道下也能及时看到（控制台本身是即时的）
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

# 项目目录 = 本脚本所在目录（code 文件夹）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# cpolar 在上一级目录的 cpolar 文件夹里
CPOLAR = os.path.join(BASE_DIR, '..', 'cpolar', 'cpolar.exe')
PORT = 8000


def port_in_use(port: int) -> bool:
    """检查本地端口是否已被占用（已占用说明 web 服务已经在跑）。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0


def main() -> None:
    print('小助手一键启动中…\n')

    # 1. 启动 web 服务（端口被占用就说明已经在跑，直接复用）
    web = None
    if port_in_use(PORT):
        print(f'[1/2] 检测到 {PORT} 端口已有服务，直接复用。')
    else:
        print('[1/2] 启动小助手服务 (web_app.py)…')
        web = subprocess.Popen(
            [sys.executable, 'web_app.py'],
            cwd=BASE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1.5)

    # 2. 启动 cpolar 隧道
    print('[2/2] 启动 cpolar 隧道…')
    cpolar = subprocess.Popen(
        [CPOLAR, 'http', str(PORT), '-region', 'cn',
         '-log', 'stdout', '-log-level', 'INFO'],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='ignore',
    )

    url_re = re.compile(r'https://[^"\s]+')
    shown = False

    def watch() -> None:
        """读 cpolar 日志，一旦出现公网地址就打印出来。"""
        nonlocal shown
        try:
            assert cpolar.stdout is not None
            for line in cpolar.stdout:
                m = url_re.search(line)
                if m and not shown:
                    shown = True
                    url = m.group(0)
                    print()
                    print('=' * 50)
                    print('  小助手已上线！手机浏览器打开：')
                    print()
                    print(f'    {url}')
                    print()
                    print('  按 Ctrl+C 退出并关闭全部服务。')
                    print('=' * 50)
                    print()
                elif 'level=error' in line.lower():
                    msg = line.split('msg=', 1)[-1].strip().strip('"')
                    print(f'[cpolar] {msg}')
        except Exception:
            pass

    threading.Thread(target=watch, daemon=True).start()
    print('（等待隧道建立，一般几秒钟…）\n')

    try:
        while cpolar.poll() is None:
            time.sleep(1)
        if not shown:
            print('\ncpolar 隧道已退出，没能建立连接。')
            print('请检查网络，或确认 cpolar 账号登录状态正常后再试。')
    except KeyboardInterrupt:
        print('\n正在关闭…')
    finally:
        for p in (cpolar, web):
            if p is not None:
                try:
                    p.terminate()
                except Exception:
                    pass
        print('已全部关闭。')


if __name__ == '__main__':
    main()
