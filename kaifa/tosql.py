##将csv文件转成Json格式传入到数据库表中
#/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import json
import csv
import codecs
import random as r
import re
import MySQLdb
import random
# import pandas as pd
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
    date = time.strftime('%Y%m%d',date_touple)
    datelist.append(date)
print (datelist)
##将csv文件转成json文件
#
csvFile = codecs.open(r"C:\Users\lulu_\Desktop\test1_nobitch.csv", "r", 'utf-8')
# jsonFile = open(r"C:\Users\lulu_\Desktop\basicinfor_nobitch.json",'w')
reader = csv.DictReader(csvFile)
hilist =[]
IP='192.168.75.251'
User_name='phpcms'
password='yuanshi1985'
database='gemini'
db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
for row in reader:
    batchid = r.choice(datelist)
    sample_data=1
    sample_id = row['样本编号']
    # print (sample_id)
    json_str=json.dumps(row,ensure_ascii=False)
    # print (json_str)
    cursor = db.cursor()
    sql="insert into ge_sample(batchid,sample_id,basic_json,sample_data) VALUES ('%s','%s','%s','%s')" % (batchid,sample_id,json_str,sample_data)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()
    # print(row)


    str1=json_str.strip()
    hilist.append(str1)


# str2 ="["+','.join(hilist)+']'
# # print (str2)
# # print (hilist)
# jsonFile.write(str2)
# jsonFile.close()



