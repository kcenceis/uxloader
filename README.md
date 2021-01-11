# uxloader
uxloader获取更新

脚本每次执行抓取每一行的URL
通过SQLlite记录是否抓取过数据,再输出到result.txt

## 安装依赖
```
pip install requests
pip install BeautifulSoup
```

# 使用方法
目录中创建uxurl.txt,然后执行
uxurl.txt中一行一个url,逐行读取
