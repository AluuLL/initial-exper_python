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

##造数据，并以csv文件形式进行保存
a1=(2018,1,1,0,0,0,0,0,0)       #设置开始日期时间元组（1976-01-01 00：00：00）
a2=(2018,6,1,23,59,59,0,0,0)  #设置结束日期时间元组（1990-12-31 23：59：59）
start=time.mktime(a1)  #生成开始时间戳
end=time.mktime(a2)   #生成结束时间戳
#随机生成10个日期字符串
datelist=[]
for i in range(100):
  t=random.randint(start,end)  #在开始和结束时间戳中随机取出一个
  date_touple=time.localtime(t)     #将时间戳生成时间元组
  # date=time.strftime("%Y年%m月%d日",date_touple) #将时间元组转成格式化字符串（1976-05-21）
  date = str(time.strftime('%Y{y}%m{m}%d{d}',date_touple).format(y='年', m='月', d='日'))
  datelist.append(date)

a1=['张','金','李','王','赵']
a2=['玉','明','龙','芳','军','玲']
a3=['','立','玲','','国','']
a4 = ['男','女']
a5 = ['小样本石蜡切片','新鲜组织']
a6 =['III期','IV期','IIIA期','IIIB期']
a7=['未知','铂类药物化疗','靶药治疗','放疗','新辅助治疗','其他药物化疗']
a8 =['MSI-S','MSI-H','MSI-L']
a9 =['小细胞肺癌','非小细胞肺癌','肺腺癌','肺鳞癌','转移性肺癌','结直肠癌']
a10 =['第二军医大学东方肝胆外科医院', '复旦大学附属中山医院', '郑州大学第一附属医院', '中国人民解放军总医院', '中山大学肿瘤防治中心 ','广西医科大学附属肿瘤医院', '空军军医大学西京医院', '四川大学华西医院', '浙江大学附属第一医院', '陆军军医大学第一附属医院', '山东省千佛山医院', '哈尔滨医科大学附属肿瘤医院', '山西省肿瘤医院', '安徽省立医院', '解放军福州总医院', '中南大学湘雅医院', '南京大学医学院附属鼓楼医院', '安徽医科大学第二附属医院', '徐州市肿瘤医院', '天津医科大学肿瘤医院', '复旦大学附属肿瘤医院', '北京大学肿瘤医院', '兰州军区兰州总医院', '厦门大学附属中山医院', '中国医学科学院肿瘤医院', '中国医科大学附属第一医院', '中山大学附属第三医院', '华中科技大学同济医学院附属同济医院', '大连医科大学第一附属医院', '福建医科大学孟超肝胆医院', '海军军医大学附属长征医院', '苏州市立医院', '广州市第一人民医院', '中国人民解放军第302医院']
a11=['CN500','NovelSeq','Hiseq']
a12=['检测到长度变异','未检测到长度变异']
#
# namelist=[]
# sexlist=[]
# agelist=[]
# samplelist=[]
# stagelist=[]
# medicinelist=[]
# msilist=[]
# diagnosislist=[]
# hospitallist=[]
# date1list=[]
list=[]
finallist=[]
batchidlist=[]
for i in range(500):
    batchid =r.choice(range(0,100,5))
    batchidlist.append(batchid)
    sampleID = i
    name=r.choice(a1)+r.choice(a2)+r.choice(a3)
    sex =r.choice(a4)
    age =r.choice(range(30,100))
    tel=r.choice(range(10000000000,99999999999))
    hospital = r.choice(a10)
    doctor = "张美玲"
    sample =r.choice(a5)
    date1 = r.choice(datelist)
    agency = "受检者未提供"
    diagnosis = r.choice(a9)
    stage = r.choice(a6)
    medicine =r.choice(a7)
    test_item= "抗肿瘤免疫治疗靶点检测"
    date2 = r.choice(datelist)
    dna =r.choice(range(3000,4000))
    plateform = r.choice(a11)
    msi =r.choice(a8)
    bat_25=r.choice(a12)
    bat_26=r.choice(a12)
    nr_21=r.choice(a12)
    nr_24=r.choice(a12)
    mono_27=r.choice(a12)

    list=[sampleID,name,sex,age,tel,hospital,doctor,sample,date1,agency,diagnosis,stage,medicine,test_item,date2,dna,plateform,msi,bat_25,bat_26,nr_21,nr_24,mono_27]
    finallist.append(list)
    print(str(sampleID)+"\t"+name+"\t"+sex+"\t"+str(age)+"\t"+str(tel)+"\t"+hospital+"\t"+doctor+"\t"+sample+"\t"+date1+"\t"+agency+"\t"+diagnosis+"\t"+stage+"\t"+medicine+"\t"+test_item+"\t"+date2+"\t"+str(dna)+"\t"+plateform+"\t"+msi+"\t"+bat_25+"\t"+bat_26+"\t"+nr_21+"\t"+nr_24+"\t"+mono_27)
m=(len(finallist))
# print (agelist)
#
with codecs.open(r"C:\Users\lulu_\Desktop\test1_nobitch.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["样本编号", "姓名", "性别","年龄","联系方式","送检医院","送检医师","送检样本","送样日期","临床诊断机构","病理诊断","分期","用药史","检测项目","收样日期","DNA总量(ng)","测序平台","MSI","BAI-25","BAT-26","NR-21","NR-24","MONO-27"])
    for i in range(m):
        writer.writerow(finallist[i])
csvfile.close()

#


##将csv文件转成json文件
#
csvFile = codecs.open(r"C:\Users\lulu_\Desktop\test1_nobitch.csv", "r", 'utf-8')
jsonFile = open(r"C:\Users\lulu_\Desktop\test1_nobitch.json",'w')
reader = csv.DictReader(csvFile)
hilist =[]
IP='192.168.75.251'
User_name='phpcms'
password='yuanshi1985'
database='gemini'
db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
for row in reader:
    batchid = r.choice(range(0, 100, 5))
    sample_data=1
    sample_id = row['样本编号']
    print (sample_id)
    json_str=json.dumps(row,ensure_ascii=False)
    print (json_str)
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


str2 ="["+','.join(hilist)+']'
# print (str2)
# print (hilist)
jsonFile.write(str2)
jsonFile.close()



