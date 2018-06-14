#往数据库中添加日期。首先随机生成时间，然后由于时间日期那一列，已经有人在数据库中增加过这一列了，
# 所以Mysql要用update来修改更新那一列，但是由于update的功能是更新修改记录为一个值。
# 若想将一列值都修改，首先要选出想要修改的那些记录，然后将每一行记录按照主键值进行Update.
#/usr/bin/python3
# -*- coding: utf-8 -*-
import random as r
import MySQLdb
import time
import random
a1=(2018,1,1,0,0,0,0,0,0)       #设置开始日期时间元组（1976-01-01 00：00：00）
a2=(2018,6,1,23,59,59,0,0,0) #设置结束日期时间元组（1990-12-31 23：59：59）
start=time.mktime(a1)  #生成开始时间戳
end=time.mktime(a2)   #生成结束时间戳
#随机生成10个日期字符串
datelist=[]
for i in range(50):
    t=random.randint(start,end)  #在开始和结束时间戳中随机取出一个
    date_touple=time.localtime(t)     #将时间戳生成时间元组
  # date=time.strftime("%Y年%m月%d日",date_touple) #将时间元组转成格式化字符串（1976-05-21）
    date = time.strftime('%Y-%m-%d %H:%M:%S',date_touple)
    datelist.append(date)
print (datelist)
hilist =[]
IP='192.168.75.251'
User_name='phpcms'
password='yuanshi1985'
database='gemini'
db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
cursor = db.cursor()
# SQL 查询语句
sql = "SELECT * FROM ge_sample WHERE sample_data=1"
try:
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        commit_bat_time=r.choice(datelist)
        home = row[0]
        sql1 = "UPDATE ge_sample SET commit_bat_time='%s' WHERE sample_uniqueid='%s'" % (commit_bat_time,home)
        try:
            cursor.execute(sql1)
            db.commit()
        except:
            db.rollback()

except:
    print("Error:unable to fetch data")

db.close()