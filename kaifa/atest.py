##统计频次信息
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
fo =open("/disk/lulu/TCGA11.txt","w")
with open(r"/disk/lulu/TCGA.txt","r") as TCGA:
    temp=[]
    for line in TCGA:
        line1 = line.strip()
        temp.append(line1)
    mytemp = sorted(set(temp))
    for item in mytemp:
        fo.write(item+"\t"+str(temp.count(item))+"\n")
        # print(item+"\t"+str(round(temp.count(item)/38,2))+"\n")

# csvFile = codecs.open(r"C:\Users\lulu_\Desktop\test1_nobitch.csv", "r", 'gbk')
# reader =csv.DictReader(csvFile)
# countprovince = []
# position=0
# realprovince=[]
# for row in reader:
#     realhospital =row['送检医院']
#     # print (realhospital)
#     # print (1)
#     csvFile1 = codecs.open(r'C:\Users\lulu_\Desktop\hospital.csv', "r", 'gbk')
#     reader1 = csv.DictReader(csvFile1)
#     for row1 in reader1:
#         province = []
#         hospital = []
#         province.append(row1['所属省份'])
#         hospital.append(row1['医院名称'])
#         # print (row['医院名称'])
#         if realhospital in row1['医院名称']:
#             position = hospital.index(row1['医院名称'])
#             # print (position)
#             realprovince = province[position]
#             countprovince.append(realprovince)
#             # print (realprovince)
#             # print (countprovince)
#             break
#
# provincelist =set(countprovince)
# for item in provincelist:
#     print (item+"\t"+str(countprovince.count(item)))
#
#
#
# csvFile = codecs.open(r'C:\Users\lulu_\Desktop\huizong.csv', "r", 'gbk')
# reader = csv.DictReader(csvFile)
# sex = []
# age = []
# diagnosis=[]
# stage=[]
# medicine=[]
# boy =[]
# girl =[]
# num1 =0
# num2 =0
# num3 =0
# num4 =0
# num5 =0
# num6 =0
# num7 =0
# num11 =0
# num21 =0
# num31 =0
# num41 =0
# num51 =0
# num61 =0
# num71 =0
# datime = []
# list1 =[]
# for row in reader:
#     sex.append(row['性别'])
#     age.append(row['年龄'])
#     if row['性别']=='男':
#         boy.append(row['年龄'])
#     if row['性别']=='女':
#         girl.append(row['年龄'])
#     diagnosis.append(row['病理诊断'])
#     stage.append(row['分期'])
#     medicine.append(row['用药史'])
#     datime.append(row['送样日期'])
# for i in datime:
#     j = i.strip().split('月')
#     k=j[0].replace('年','.')
#     list1.append(k)
# mylist1 = set(list1)
# for item in sorted(mylist1):
#     print (item+"\t"+str(list1.count(item)))
#
# mydiagnosis = list(set(diagnosis))
# mystage = list(set(stage))
# mymedicine = list(set(medicine))
#
# for item in mydiagnosis:
#     print (item+"\t"+str(diagnosis.count(item)))
#
# for i in mystage:
#     print (i + "\t"+str(stage.count(i)))
#
# for j in mymedicine:
#     print (j + "\t"+ str(medicine.count(j)))
#
# for i in boy:
#     if 30<=int(i)<40:
#         num1=num1+1
#     if 40<=int(i)<50:
#         num2=num2+1
#     if 50<=int(i) <60:
#         num3=num3+1
#     if 60<=int(i)<70:
#         num4=num4+1
#     if 70<=int(i)<80:
#         num5=num5+1
#     if 80<=int(i)<90:
#         num6=num6+1
#     if 90<=int(i)<100:
#         num7=num7+1
# print ('男'+"\t"+"[30,40)"+"\t"+str(num1))
# print ('男'+"\t"+"[40,50)"+"\t"+str(num2))
# print('男' + "\t"+"[50,60)"+"\t"+str(num3))
# print('男' +"\t"+"[60,70)"+"\t"+ str(num4))
# print('男' +"\t"+"[70,80)"+"\t"+ str(num5))
# print('男' +"\t"+"[80,90)"+"\t"+ str(num6))
# print('男' +"\t"+"[90,100)"+"\t"+ str(num7))
# for i in girl:
#     if 30<=int(i)<40:
#         num11=num11+1
#     if 40<=int(i)<50:
#         num21=num21+1
#     if 50<=int(i) <60:
#         num31=num31+1
#     if 60<=int(i)<70:
#         num41=num41+1
#     if 70<=int(i)<80:
#         num51=num51+1
#     if 80<=int(i)<90:
#         num61=num61+1
#     if 90<=int(i)<100:
#         num71=num71+1
# print ('女'+"\t"+"[30,40)"+"\t"+str(num11))
# print ('女'+"\t"+"[40,50)"+"\t"+str(num21))
# print('女' +"\t"+"[50,60)"+"\t"+ str(num31))
# print('女' + "\t"+"[60,70)"+"\t"+str(num41))
# print('女' +"\t"+"[70,80)"+"\t"+ str(num51))
# print('女' +"\t"+"[80,90)"+"\t"+ str(num61))
# print('女' +"\t"+"[90,100)"+"\t"+ str(num71))
#
#
