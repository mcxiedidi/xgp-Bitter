import pickle
import random
import os
import hashlib
import platform
import zipfile
import requests
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

gonggaourl = 'http://payback.maomc.asia/xgp/gonggao.txt'
gonggao_data = requests.get(gonggaourl)
gonggao_data.encoding = 'utf-8'
gonggao = gonggao_data.text
banbenurl = 'http://payback.maomc.asia/xgp/ver.txt'
banben_data = requests.get(banbenurl)
banben_data.encoding = 'utf-8'
banben = banben_data.text
nowbanben = '1.2.3'


def logo():
    print(' _________  ________ _____ ______   ________ ')
    print('|\___   ___\\  _____\\   _ \  _   \|\   ____\  ')
    print('\|___ \  \_\ \  \__/\ \  \\\__\ \  \ \  \___|    ')
    print('     \ \  \ \ \   __\\ \  \\|__| \  \ \  \       ')
    print('      \ \  \ \ \  \_| \ \  \    \ \  \ \  \____  ')
    print('       \ \__\ \ \__\   \ \__\    \ \__\ \_______\ ')
    print('        \|__|  \|__|    \|__|     \|__|\|_______|')


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


def noupdata():
    print(' _________  ________ _____ ______   ________ ')
    print('|\___   ___\\  _____\\   _ \  _   \|\   ____\  ')
    print('\|___ \  \_\ \  \__/\ \  \\\__\ \  \ \  \___|    ')
    print('     \ \  \ \ \   __\\ \  \\|__| \  \ \  \       ')
    print('      \ \  \ \ \  \_| \ \  \    \ \  \ \  \____  ')
    print('       \ \__\ \ \__\   \ \__\    \ \__\ \_______\ ')
    print('        \|__|  \|__|    \|__|     \|__|\|_______|')
    print('公告:' + gonggao)
    print('======= Xgp =======')
    print('=== Version ' + nowbanben + ' ===')
    print('更新完成，最新版本：' + banben + '.zip 请到new文件夹找到start.py替换根目录')


def newupdata():
    print(' _________  ________ _____ ______   ________ ')
    print('|\___   ___\\  _____\\   _ \  _   \|\   ____\  ')
    print('\|___ \  \_\ \  \__/\ \  \\\__\ \  \ \  \___|    ')
    print('     \ \  \ \ \   __\\ \  \\|__| \  \ \  \       ')
    print('      \ \  \ \ \  \_| \ \  \    \ \  \ \  \____  ')
    print('       \ \__\ \ \__\   \ \__\    \ \__\ \_______\ ')
    print('        \|__|  \|__|    \|__|     \|__|\|_______|')
    print('公告:' + gonggao)
    print('======= Xgp =======')
    print('=== Version ' + nowbanben + ' ===')
    print('目前为最新版本，无需更新')


qianzhui = 'qianzhui.txt'


def generate_prefix_file():
    print('[+]初始化前缀')
    with open(qianzhui, 'w') as f:
        f.write('TFMC_')
    print('[+]初始化完成')


if not os.path.exists(qianzhui):
    generate_prefix_file()
with open('qianzhui.txt', 'r') as f:
    prefixes = [line.strip() for line in f]

def restart():
  python = sys.executable
  os.execl(python, python, * sys.argv)


def randomAccount(length=16):
    base_Str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_'
    random_str = ''
    for i in range(length):
        random_str += base_Str[random.randint(0, (len(base_Str) - 1))]
    qian = random.choice(prefixes)
    return qian + random_str


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument ('--incognito')
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 禁用图片加载
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
if nowbanben != banben:
    # 下载新版本压缩包
    print('检测到最新版本' + banben + ',正在下载......')
    url = f"http://payback.maomc.asia/xgp/{banben}.zip"
    response = requests.get(url)
    zip_file_path = f"{banben}.zip"

    with open(zip_file_path, 'wb') as zip_file:
        zip_file.write(response.content)
    # 尝试解压
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                file_info.filename = file_info.filename.encode('cp437').decode('gbk')
                zip_ref.extract(file_info)
    except zipfile.BadZipFile:
        print("下载的文件不是有效的 ZIP 压缩文件")
        os.remove(zip_file_path)
        exit()
    # 删除压缩文件
    os.remove(zip_file_path)
    noupdata()
if nowbanben == banben:
    newupdata()
print('开始验证授权......')
url = "http://payback.maomc.asia/xgp/hwid.txt"
hwid_list = load_hwid_from_url(url)
validate_hwid(hwid_list)
try:
    while True:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 360)
        ltwait = WebDriverWait(driver, 5)
        zhwait = WebDriverWait(driver, 5)
        test = WebDriverWait(driver, 10)
        mmwait = WebDriverWait(driver, 60)
        ccwait = WebDriverWait(driver, 180)
        name = randomAccount(6)
        with open("../cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        with open('zfbpwd.txt', 'r') as f:
            zfbpwd = f.readline().strip()
        try:
            with open('acc.txt', 'r') as file:
                num_lines = sum(1 for line in file)
        except:
            print('[-]账号文件为空')
            driver.quit()
        with open('acc.txt', 'r') as f:
            lines = f.readlines()
            account, password = lines[0].strip().split(':')
        print('账号管理器| 账号数量：' + str(len(lines)))
        print('账号管理器| 当前账号：' + account)
        print('支付宝|    准备导入ck')
        driver.get('https://www.alipay.com/')
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        print('支付宝|    导入ck完成')
        driver.get('https://www.xbox.com/zh-HK/auth/msa?action=logIn&returnUrl=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%3FlaunchStore%3DCFQ7TTC0KGQ8%23join&cobrandid=e5ada363-6ac5-4c74-bc19-d8ed821aa5fd')
        newurl = 'https://www.minecraft.net/en-us/msaprofile/redeem?setupProfile=true'
        driver.execute_script(f"window.open('{newurl}', '_blank');")
        driver.switch_to.window(driver.window_handles[0])
        email_box = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
        email_box.send_keys(account)
        butt1 = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                             "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input")))
        butt1.click()
        password_box = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
        password_box.send_keys(password)
        bott2 = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
        bott2.click()
        try:
            skip = driver.find_element('id', 'iShowSkip')
            # 执行需要执行的代码
            skip.click()
        except:
            # 如果找不到元素，则跳过执行
            print('账号管理器| 已跳过邮箱系统')
        try:
            skip2 = driver.find_element('id', 'iCancel')
            # 执行需要执行的代码
            skip2.click()
        except:
            # 如果找不到元素，则跳过执行
            print('账号管理器| 已跳过 安全绑定')
        try:
            skip = driver.find_element('id', 'iShowSkip')
            # 执行需要执行的代码
            skip.click()
        except:
            # 如果找不到元素，则跳过执行
            print('账号管理器| 已跳过邮箱系统')
        try:
            element = ltwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#StartHeader.text-title[role='heading'][aria-level='1']")))
            print('账号管理器| 该账号已封禁')
            driver.quit()
            with open('acc.txt', 'w') as f:
                f.writelines(lines[1:])
            break
        except:
            print('账号管理器| 账号正常，继续操作')
        bott3 = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
        # bott3 = driver.find_element('id','idSIButton9')
        bott3.click()
        try:
            skip2 = driver.find_element('id', 'iCancel')
            # 执行需要执行的代码
            skip2.click()
        except:
            # 如果找不到元素，则跳过执行
            print('账号管理器| 已跳过 安全绑定')
        try:
            skip3 = driver.find_element('id', 'iShowSkip')
            # 执行需要执行的代码
            skip3.click()
        except:
            # 如果找不到元素，则跳过执行
            print('账号管理器| 已跳过邮箱系统')
        try:
            skip4 = driver.find_element('id', 'iCancel')
            # 执行需要执行的代码
            skip4.click()
        except:
            # 如果找不到元素，则跳过执行
            print('账号管理器| 已跳过 安全绑定')
        # 输入用户名
        print('账号管理器| 已登录：' + account)
        username = mmwait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/main/div[1]/div[2]/div/div[5]/div/div[1]/div[1]/button")))
        print('账号管理器| 开始设置用户名')
        time.sleep(5)
        username.click()
        time.sleep(5)
        okname = wait.until(EC.visibility_of_element_located((By.ID, 'inline-continue-control')))
        okname.click()
        print('账号管理器| 设置完成')
        print('订阅| 开始订阅')
        # 点击下一步
        butt6 = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div[4]/div/div[2]/button')))
        butt6.click()
        # 添加付款方式
        iframe = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/iframe")))
        # 进入iframe区块
        driver.switch_to.frame(iframe)
        time.sleep(2)
        butt7 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/section/div[1]/div/div/div/div/div[2]/div/div[3]/div[2]/button')))
        butt7.click()
        try:
            test1 = test.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/section/div[1]/div/div/div/div/div[2]/div/div[3]/div/button")))
            test1.click()
            butt8 = wait.until(EC.visibility_of_element_located((By.ID, 'displayId_ewallet')))
            butt8.click()
        except:
            butt8 = wait.until(EC.visibility_of_element_located((By.ID, 'displayId_ewallet')))
            butt8.click()
            # 选择支付宝
        butt9 = wait.until(EC.visibility_of_element_located((By.ID, 'displayId_ewallet_alipay_billing_agreement')))
        butt9.click()
        butt10 = wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-button-saveNextButton')))
        butt10.click()
        # 进入支付宝签约页面
        butt11 = wait.until(
            EC.visibility_of_element_located((By.ID, 'pidlddc-hyperlink-alipayQrCodeChallengeRedirectionLink')))
        butt11.click()
        # 切换页面
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[2])
        # 输入支付宝支付密码
        try:
            alpaypwd = wait.until(EC.visibility_of_element_located((By.ID, 'payPassword_rsainput')))
            alpaypwd.send_keys(zfbpwd)
            time.sleep(5)
            jixu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'J_submit')))
            driver.execute_script("arguments[0].click();", jixu)
            time.sleep(5)
        except:
            # 定位不到
            print('可能是以下原因:')
            print('支付宝登录失效 请启动zfbck.py 更新支付宝ck')
            print('程序未点击到按钮')
        # 进入iframe区块
        fanhui = wait.until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/a")))
        driver.close()
        # 切换到前一页面
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.frame(iframe)
        time.sleep(2)
        butt77 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/section/div[1]/div/div/div/div/div/div[2]/section/div[3]/input[2]')))
        butt77.click()
        try:
            dz4 = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='city']")))
            dz4.send_keys('厕')
            dz5 = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='address_line1']")))
            dz5.send_keys('所')
            dz6 = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='pidlddc-button-saveButton']")))
            dz6.click()
            print('订阅| 地区设定完成')
        except:
            print('订阅| 无地区设定')
        dingyue = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='store-cart-root']/div/div/div[2]/div/div[4]/button[2]")))
        dingyue.click()
        time.sleep(5)
        try:
            xiazai = ccwait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div[3]/a")))
        except:
            print('订阅| 首次检测失败，正在进行第二轮')
            time.sleep(10)
            xiazai = ccwait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div[3]/a")))
        print('订阅| 订阅完成')
        driver.get('https://account.microsoft.com/services/pcgamepass/details#billing')
        print('我的世界| 开始命名我的世界游戏名')
        driver.switch_to.window(driver.window_handles[1])
        # 点击登录
        dl = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div/div[1]/div[1]/div[1]/a")))
        dl.click()
        # 设置用户名
        mcname = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='profileNameLabel']/input")))
        mcname.send_keys(name)
        szyhm = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div/main/section/div/div/section/div[2]/form/div/div[2]/button")))
        szyhm.click()
        try:
            jinru = ltwait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='main-content']/section/div/div/section/div[2]/div/button[2]")))
        except:
            print('我的世界| 命名重复')
            def randomAccount(length=16):
                base_Str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_'
                random_str = ''
                for i in range(length):
                    random_str += base_Str[random.randint(0, (len(base_Str) - 1))]
                qian = random.choice(prefixes)
                return qian + random_str
            rename = randomAccount(6)
            mcname = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='profileNameLabel']/input")))
            mcname.send_keys(Keys.CONTROL + 'a')
            mcname.send_keys(Keys.DELETE)
            mcname.send_keys(rename)
            szyhm = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div/main/section/div/div/section/div[2]/form/div/div[2]/button")))
            szyhm.click()
            print('我的世界| 重命名完成')
        jinru = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='main-content']/section/div/div/section/div[2]/div/button[2]")))
        jinru.click()
        print('我的世界| 命名成功')
        print('我的世界| 命名完成')
        print('支付宝| 开始退款')
        driver.switch_to.window(driver.window_handles[0])
        # 继续
        try:
            time.sleep(3)
            next2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='id__0']")))
            next2.click()
        except:
            print('系统| 无限制')
        # 订阅退订
        dytd = wait.until(EC.visibility_of_element_located((By.ID, 'cancel-sub-button')))
        dytd.click()
        time.sleep(6)
        dytd1 = wait.until(EC.visibility_of_element_located((By.ID, 'benefit-cancel')))
        dytd1.click()
        quxiao2 = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Cancel now and get refund']")
        quxiao2.click()
        dytd3 = wait.until(EC.visibility_of_element_located((By.ID, 'cancel-select-cancel')))
        dytd3.click()
        dytd4 = wait.until(EC.visibility_of_element_located((By.ID, 'confirm-back-to-subscription-button')))
        dytd4.click()
        print('支付宝| 退款完成')
        driver.get('https://account.microsoft.com/billing/payments')
        print('支付宝| 取消关联')
        time.sleep(3)
        qxgl = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div/div/div/main/div[2]/div[2]/div[4]/div/div[2]/div/div/div[2]/div[3]/div/button/span/div')))
        qxgl.click()
        time.sleep(3)
        qxgl1 = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/button[2]')))
        qxgl1.click()
        time.sleep(3)
        qxgl2 = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[4]/div/button')))
        qxgl2.click()
        print('支付宝| 取消完成')
        # 写入刷完的账号
        time6 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with open('newacc.txt', 'a') as f:
            f.write(f'{account}|{password}|{name}|{time6}\n')
        # 从源里删除刷完的
        with open('acc.txt', 'w') as f:
            f.writelines(lines[1:])
        print('系统| 下一张')
        driver.close()
        driver.quit()
    print('系统| 开始重启')
    restart()
except:
    print('[!]系统错误！！！！，请把err_screen.png给我看好嘛！')
    driver.save_screenshot('err_screen.png')
