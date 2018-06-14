##统计医院信息
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
import pandas as pd
import xlrd

#将表格形式转成csv文件形式
# data_xls = pd.read_excel(r'/disk/lulu/hospital_site.xlsx',index_col=0)
# data_xls.to_csv('/disk/lulu/hospital.csv',encoding='utf-8')

csvFile1 = codecs.open(r'C:\Users\lulu_\Desktop\huizong.csv', "r", 'gbk')
csvFile = codecs.open(r'C:\Users\lulu_\Desktop\hospital_site.csv', "r", 'gbk')
reader1 =csv.DictReader(csvFile1)
reader = csv.DictReader(csvFile)
province =[]
hospital = []
countprovince = []
for row1 in reader1:
    realhospital =row1['送检医院']
    for row in reader:
        province.append(row['所属省份'])
        hospital.append(row['医院名称'])
    if realhospital in hospital:
            position = hospital.index(realhospital)
    realprovince = province[position]
    countprovince.append(realprovince)
provincelist =set(countprovince)
for item in provincelist:
    print (item+"\t"+countprovince(item))
