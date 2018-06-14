# -*- coding: utf-8 -*-
#实现系统管理页面的另一种方法
import json
import MySQLdb
import time
import datetime

def system_result():
    global dict
    dict ={}
    summary()
    # print (dict)
    judge(dict)
    status =json.dumps(dict,ensure_ascii=False)
    # print (status)
    return status

def judge(dict):
    exportlist=[]
    for i in range(0,len(dict['export'])):
        exportlist.append(dict['export'][i]['name'])
    # print (exportlist)
    analysislist=[]
    for i in range(0,len(dict['analysis'])):
        analysislist.append(dict['analysis'][i]['name'])
    # print (analysislist)
    forexportlist=sorted(list(set(analysislist).difference(set(exportlist)))) # analysislist中有而exportlist中没有的
    # print (forexportlist)
    foranalysislist=sorted(list(set(exportlist).difference(set(analysislist))))# exportlist中有而analysislist中没有的
    # print (foranalysislist)
    for item in forexportlist:
        temp = {"name": item, "value": 0}
        dict["export"].append(temp)
    for item in foranalysislist:
        temp = {"name":item,"value":0}
        dict["analysis"].append(temp)
    return dict


    # print(len(dict['export']))
    # print (dict['analysis'])

def summary():
    IP = '192.168.75.251'
    User_name = 'phpcms'
    password = 'yuanshi1985'
    database = 'gemini'

    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # sql = "select commit_time(time,'%Y-%m-%d') from ge_task WHERE status=4 or status=5"
    # sql = "select commit_time from ge_task WHERE status=4 or status=5"
    sql = "select date_format(log_time, '%Y-%m-%d' ) as post_date_log from ge_reportlog WHERE status=5 ORDER BY log_time"
    try:
        # export
        cursor.execute(sql)
        results = cursor.fetchall()
        rowlist1 = []
        for row1 in results:
            rowlist1.append(row1[0])
        #     print (row1[0])
        # print (rowlist1)
    except:
        print("Error: unable to fetch data")
    db.close()


    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # sql = "select commit_time(time,'%Y-%m-%d') from ge_task WHERE status=4 or status=5"
    # sql = "select commit_time from ge_task WHERE status=4 or status=5"
    sql ="select date_format(commit_time, '%Y-%m-%d' ) as post_date_gmt from ge_task WHERE status=4 or status=5 ORDER BY commit_time"
    try:
        # analysis
        cursor.execute(sql)
        results = cursor.fetchall()
        rowlist = []
        for row in results:
            # print ("1")
            rowlist.append(row[0])
            # print (row[0])
        # print (rowlist)
    except:
        print("Error: unable to fetch data")
    db.close()

    # #
    tempmylsit1 = []
    mylist1 = sorted(list(set(rowlist1)))
    tempmylsit=[]
    mylist =sorted(list(set(rowlist)))
    alllist=sorted(set(mylist1+mylist))
    for item1 in alllist:
        temp1 = {"name": item1, "value": rowlist1.count(item1)}
        tempmylsit1.append(temp1)
    dict["export"] = tempmylsit1


    for item in alllist:
        temp = {"name": item, "value": rowlist.count(item)}
        tempmylsit.append(temp)
    dict["analysis"] = tempmylsit
    print (dict)


if __name__ == '__main__':

    system_result()