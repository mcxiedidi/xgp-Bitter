import hashlib
import os
import platform
import requests
import sys
import time
import logging
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_hwid():
    hwid = platform.node() + platform.processor() + platform.architecture()[0]
    return hashlib.md5(hwid.encode()).hexdigest()

def load_hwid_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        hwid_list = response.text.strip().split("\n")
        return hwid_list
    else:
        print("无法连接到HWID服务器")
        return []

def save_hwid(hwid):
    with open("hwid.txt", "w") as file:
        file.write(hwid)

def load_hwid():
    if os.path.exists("hwid.txt"):
        with open("hwid.txt", "r") as file:
            return file.read().strip()
    return None

def validate_hwid(hwid_list):
    current_hwid = get_hwid()
    save_hwid(current_hwid)  # 保存当前的HWID
    if current_hwid in hwid_list:
        print("HWID验证成功")
    else:
        print("HWID验证失败")
        print("本机HWID:", current_hwid)
        print("请联系QQ3108887050添加授权")
        sys.exit()

url = "https://blog.tfmc.cc/xgp/hwid.txt"
print('欢迎使用支付宝CK更新器')
print('开始验证授权......')
hwid_list = load_hwid_from_url(url)
validate_hwid(hwid_list)
zfburl = 'https://auth.alipay.com/login/index.htm?goto=https%3A%2F%2Fwww.alipay.com%2F'
bd = 'https://www.baidu.com/'
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-blink-features")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get(bd)
time.sleep(3)
driver.get(zfburl)
print('请在30秒内登录')
time.sleep(30)
while True:
    # 刷新Ck
    driver.refresh()
    # 获取Cookie
    cookies = driver.get_cookies()
    # 将Cookie写入文件
    with open("cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)
    print('ck获取成功')
    # 等待3分钟
    time.sleep(180)
