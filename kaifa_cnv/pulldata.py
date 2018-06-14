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
import pandas as pd

IP='192.168.75.251'
User_name='phpcms'
password='yuanshi1985'
database='gemini'
db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
cursor = db.cursor()
sql = "select batchid,basic_json,sample_data from ge_sample WHERE sample_data=1"
try:
    rowlist=[]
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        rowlist.append(row)

except:
    print ("Error: unable to fetch data")

db.close()

