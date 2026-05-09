import shutil
from urllib.request import build_opener, HTTPSHandler, install_opener, Request, urlopen
import ssl
import re
import os

context = ssl._create_unverified_context()
opener = build_opener(HTTPSHandler(context=context))
install_opener(opener)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"

def get_response(url):
    res = Request(url , headers={'User-Agent':user_agent})
    def inner():
        return urlopen(res).read().decode("utf-8")
    return inner

def download_image(url,img_path):
    img_data = Request(url, headers={'User-Agent': user_agent})
    img_data = urlopen(img_data).read()

    with open(img_path, 'wb') as f:
        f.write(img_data)
        print("图片下载成功！")

html_func = get_response("https://www.bizhihui.com/dongman/2/")
html_content = html_func()  

regex = '''<img src="(.*?)-pcthumbs" alt="(.*?)" width="450" height="285">'''

ret = re.findall(regex, html_content)

if os.path.isdir("images"):
    shutil.rmtree("images")

os.mkdir("images")

for i in ret:
    file_ext = i[0].split(".")[-1]
    url_path = f"images{os.sep}{i[1].replace(' ', '_')}.{file_ext}"
    download_image(i[0], url_path)
    print(url_path + "已保存！")

print("图片下载结束！")