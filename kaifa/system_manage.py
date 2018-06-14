# -*- coding: utf-8 -*-
import json
import MySQLdb
import time
import datetime
import itertools


def system_result():
    global dict
    finaldict={}
    dict ={}
    dict1={}
    dict2={}
    analysis()
    export()
    # print (dict)
    judge(dict)
    list=dict["analysis"]
    # print (list)
    allnamelist=[]
    allvaluelist=[]
    namelist=[]
    valuelist=[]
    new_dict={}
    for i in list:
        namelist=i["name"]
        valuelist=i["value"]
        allnamelist.append(namelist)
        allvaluelist.append(valuelist)
    # print (allnamelist)
    # print (allvaluelist)
    i=0
    length =len(allvaluelist)
    while i<length:
        dit ={allnamelist[i]:allvaluelist[i]}
        new_dict.update(dit)
        i+=1
    dict1["analysis"] = []
    tempanalysislist = []
    for key in sorted(new_dict.keys()):
        # print (key,new_dict[key])
        temp = {"name": key, "value": new_dict[key]}
        tempanalysislist.append(temp)
    finaldict["analysis"] = tempanalysislist


    # #######

    list1=dict["export"]
    # print (list1)
    allnamelist1=[]
    allvaluelist1=[]
    namelist1=[]
    valuelist1=[]
    new_dict1={}
    for i in list1:
        namelist1=i["name"]
        valuelist1=i["value"]
        allnamelist1.append(namelist1)
        allvaluelist1.append(valuelist1)
    # print (allnamelist1)
    # print (allvaluelist1)
    j=0
    length1 =len(allvaluelist1)
    while j<length1:
        dit1 ={allnamelist1[j]:allvaluelist1[j]}
        new_dict1.update(dit1)
        j+=1
    dict2["export"] = []
    tempexportlist = []
    for key in sorted(new_dict1.keys()):
        # print (key,new_dict1[key])
        temp = {"name": key, "value": new_dict1[key]}
        tempexportlist.append(temp)
    finaldict["export"] = tempexportlist

    status =json.dumps(finaldict,ensure_ascii=False)
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

    foranalysislist=sorted(list(set(exportlist).difference(set(analysislist))))# exportlist中有而analysislist中没有的
    for item in forexportlist:
        temp = {"name": item, "value": 0}
        dict["export"].append(temp)
    for item in foranalysislist:
        temp = {"name":item,"value":0}
        dict["analysis"].append(temp)

    # print (sorted(dict["analysis"].keys()))
    return dict


    # print(len(dict['export']))
    # print (dict['analysis'])

def export():
    # IP = '192.168.75.251'
    IP ='127.0.0.1'
    User_name = 'phpcms'
    password = 'yuanshi1985'
    database = 'gemini'

    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # sql = "select commit_time(time,'%Y-%m-%d') from ge_task WHERE status=4 or status=5"
    # sql = "select commit_time from ge_task WHERE status=4 or status=5"
    sql = "select date_format(log_time, '%Y-%m-%d' ) as post_date_log from ge_reportlog WHERE status=5 ORDER BY log_time"
    try:
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

    # #
    tempmylsit1 = []
    mylist1 = sorted(list(set(rowlist1)))
    # print (mylist1)
    for item1 in mylist1:
        temp1 = {"name": item1, "value": rowlist1.count(item1)}
        tempmylsit1.append(temp1)
    dict["export"] = tempmylsit1


def analysis():
    # IP = '192.168.75.251'
    IP ='127.0.0.1'
    User_name = 'phpcms'
    password = 'yuanshi1985'
    database = 'gemini'

    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # sql = "select commit_time(time,'%Y-%m-%d') from ge_task WHERE status=4 or status=5"
    # sql = "select commit_time from ge_task WHERE status=4 or status=5"
    sql ="select date_format(commit_time, '%Y-%m-%d' ) as post_date_gmt from ge_task WHERE status=4 or status=5 ORDER BY commit_time"
    try:
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
    # datime = []
    # alldata=[]
    # dict = {}
    tempmylsit=[]
    mylist =sorted(list(set(rowlist)))
    for item in mylist:
        temp = {"name": item, "value": rowlist.count(item)}
        tempmylsit.append(temp)
    dict["analysis"] = tempmylsit
    # print (dict)

#
# if __name__ == '__main__':
#
#     system_result()