import sqlite3
import os

SQLDATABASEFILE = os.path.split(os.path.realpath(__file__))[0]+ os.sep +'uxurl.db'  # 数据库文件名称


def connSQL():
    if not os.path.exists(SQLDATABASEFILE):  # 检查是否存在表
        conn = sqlite3.connect(SQLDATABASEFILE)
        print('Opened database successfully');
        c = conn.cursor()

        # 执行创建表
        c.execute('''CREATE TABLE uxhistory                      
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       ADDRESS        CHAR(50),
       FILENAME          CHAR(200),
       fDate         CHAR(200),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        # 插入数据表
        conn.commit()
        c.close()
        conn.close()


def insertSQL(mAddress, mFILENAME, mDate):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("INSERT INTO uxhistory (ADDRESS,FILENAME,fDate) \
      VALUES (?,?,?)", (mAddress, mFILENAME, mDate,));
    conn.commit()
    c.close()
    conn.close()


# 获取count，查看是否存在相同条目，返回bool
def HAS_SQL(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from uxhistory where ADDRESS = ?", (mAddress,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False
