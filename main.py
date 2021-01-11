import os

import requests
from bs4 import BeautifulSoup
import re
import time
import SQLUTILS

isPROXY = False  # 定义是否开启代理
proxies = {'http': 'socks5://127.0.0.1:1082',
           'https': 'socks5://127.0.0.1:1082'}  # 代理端口为1082
SQLUTILS.connSQL()  # 检查是否存在数据库

params = {"q": "age_confirmation"}
urllist = []
filePath = os.path.split(os.path.realpath(__file__))[0]  # 获取脚本当前目录

for line in open(filePath+os.sep+"uxurl.txt"):  # 读取uxurl.txt的ux网址
    urllist.append(line.strip())
patternForTime = r'(\d{2}/\d{1,2}/\d{1,2}\s\d{1,2}:\d{1,2})'  # 日期通配符

isNewRequests = True
session = requests.session()


# 定义以URL获取数据  例子https://ux.getuploader.com/kisakikiki/
def getNewMod(url):
    fileurllist = []
    filenamelist = []
    filedate = []
    if isNewRequests:
        if isPROXY:
            # r = session.post(url=url, headers=headers, proxies=proxies, data=params)  # 执行requests
            r = session.post(url=url, proxies=proxies, data=params)  # 执行requests
        else:
            # r = session.post(url=url, headers=headers, data=params)  # 执行requests
            r = session.post(url=url, data=params)  # 执行requests
    else:
        if isPROXY:
            r = session.get(url=url, proxies=proxies)
        else:
            r = session.get(url=url)
    # cookies = requests.utils.dict_from_cookiejar(r.cookies)
    print(r.text)

    soup = BeautifulSoup(r.text, 'html.parser')  # 提取html内容
    if soup.find_all('h1')[0].text == '年齢確認':
        raise ValueError('cookies过期')  # 防止cookie过期
    tbodysoup = soup.find('tbody')
    newsoup = BeautifulSoup(str(tbodysoup), 'html.parser')
    for kk in newsoup.find_all('a'):
        if re.search(r'/download/', str(kk)):
            fileurl = kk['href']  # 获取新mod的URL
            filename = kk.text  # 获取新mod的name
            fileurllist.append(fileurl)
            filenamelist.append(filename)
    for kk in soup.find_all('td'):
        if re.search(patternForTime, str(kk)):  # 获取新mod时间
            filedate.append(kk.text)
    for i in range(0, len(fileurllist)):
        thisurl = str(fileurllist[i])
        thisname = str(filenamelist[i])
        thisdate = str(filedate[i])
        if not SQLUTILS.HAS_SQL(thisurl):  # 读取database,查看是否有重复URL,因URL为独一无二
            SQLUTILS.insertSQL(thisurl, thisname, thisdate)  # 写入到database,防止重复数据
            f = open(filePath+os.sep+r"reuslt.txt", 'a', encoding='UTF-8')  # 把获取到的数据,追加写入到result.txt
            txt = thisurl + "   name:" + thisname + "  date:" + thisdate
            f.write(txt + '\r')
            f.close()


try:
    # 执行主方法
    for ur in urllist:
        getNewMod(ur)
        time.sleep(2)  # 防止高速抓取数据导致封IP,默认1s延迟执行一次抓取
        # 判断是否是新连接
        if isNewRequests:
            isNewRequests = False
except IndexError as e:
    print(e)
    f = open(filePath+os.sep+r"error.log", 'a', encoding='UTF-8')  # 输出error.log
    f.write(ur + '\r')
    f.write(e + '\r')
    f.close()
except ValueError as e:
    print(e)
    f = open(filePath+os.sep+r"error.log", 'a', encoding='UTF-8')  # 输出error.log
    f.write(str(e) + '\r')
    f.close()
