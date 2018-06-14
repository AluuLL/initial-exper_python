#/usr/bin/python3
# -*- coding: utf-8 -*-
# 线下版本
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
from datetime import datetime,timedelta
import math


def label_result(data):
    # if data["性别"] == [] and data["年龄"] == [] and data['病理诊断'] == [] and data['病人批次'] == []:
    if data["性别"] == [] and data["年龄"] == [] and data['病理诊断']==[] and data['病人批次']["min"]==0 and data['病人批次']["max"]==0:
        rowlist = fromsql()
        status=all_display(rowlist)
        # print(status)
        return status
    else:
        #筛选病人批次，以及筛选其他值的情况
        # if data['病人批次']：
        if data['病人批次']["min"]!="" or data['病人批次']["max"]!="":
            # if len(data['病人批次'])==2:
            if data['病人批次']["min"] != "" and data['病人批次']["max"] != "":
                # batchdatelist=getEveryDay(data['病人批次'][0], data['病人批次'][1])
                begin_date=data['病人批次']["min"]
                end_date=data['病人批次']["max"]
                rowlist=forbatchsql(begin_date,end_date)
                # print (rowlist)
                if rowlist:
                    sexvalue_list=data['性别']
                    agevalue_list=data['年龄']
                    diagnosisvalue_list=data['病理诊断']
                    # print (sexvalue_list)
                    # print (agevalue_list)
                    # print (diagnosisvalue_list)
                    # print (data['病人批次'])
                    status = batch_part_display(rowlist,sexvalue_list,agevalue_list,diagnosisvalue_list)
                    # print(status)
                    return status

                else:
                    return ("None")

            else:
                if data['病人批次']['min']=="":
                    begin_date="2017-01-01"
                    end_date=data['病人批次']["max"]
                if data['病人批次']["max"]=="":
                    begin_date =data['病人批次']["min"]
                    end_date =time.strftime('%Y-%m-%d',time.localtime(time.time()))
                rowlist = forbatchsql(begin_date,end_date)
                if rowlist:
                    # status = all_display(rowlist)
                    sexvalue_list = data['性别']
                    agevalue_list = data['年龄']
                    diagnosisvalue_list = data['病理诊断']
                    # print (sexvalue_list)
                    # print (agevalue_list)
                    # print (diagnosisvalue_list)
                    # print (data['病人批次'])
                    # status='lulu'
                    status = batch_part_display(rowlist, sexvalue_list, agevalue_list, diagnosisvalue_list)
                    # print(status)
                    return status

                else:
                    return ("None")

        else:
            rowlist=fromsql()
            if rowlist:
                sexvalue_list = data['性别']
                agevalue_list = data['年龄']
                diagnosisvalue_list = data['病理诊断']
                # print (sexvalue_list)
                # print (agevalue_list)
                # print (diagnosisvalue_list)
                # status='lulu'
                status = batch_part_display(rowlist, sexvalue_list, agevalue_list, diagnosisvalue_list)
                # print(status)
                return status
            else:
                return ("None")

        #没有筛选病人批次，筛选其他值的情况
        # elif:

    # if not list(data.values()):#若字典为空，也就
                # 是未初始化的情况下。
    #     all_display(data)
    # if data:
    #     print('lulu')
    # print (data['性别'])

def batch_part_display(rowlist,sexvalue,agevalue,diagnosisvalue):
    # print (sexvalue)
    # print (agevalue)
    # print (diagnosisvalue)
    # print (rowlist)
    if (sexvalue==['男','女'] or sexvalue==[]) and (agevalue==[] or agevalue==["0","125"]) and (diagnosisvalue==[] or diagnosisvalue ==['非小细胞肺癌','小细胞肺癌','非鳞性非小细胞肺癌','肺鳞癌','肺腺癌','非腺鳞癌','大细胞癌']):
        dict = {}
        batchidlist = []
        basiclist = []
        sex = []
        age = []
        diagnosis = []
        stage = []
        medicine = []
        boy = []
        girl = []
        num0 = 0
        num01 = 0
        num02 = 0
        num10 = 0
        num101 = 0
        num102 = 0
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0
        num7 = 0
        num11 = 0
        num21 = 0
        num31 = 0
        num41 = 0
        num51 = 0
        num61 = 0
        num71 = 0
        datime = []
        diagnosis = []
        stage = []
        medicine = []
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        list7 = []
        list8 = []
        list9 = []
        list10 = []
        list11 = []
        list12 = []
        list13 = []
        list14 = []
        list15 = []
        list16 = []
        list17 = []
        list18 = []
        list19 = []
        list20 = []
        list21 = []
        list22 = []
        msi = []
        samplename = []
        # 箱线图
        pathlist = []

        hospital = []
        for item in rowlist:
            # print (item[1])
            batchidlist.append(item[0])
            basiclist.append(item[1])
            dictitem = json.loads(item[1])
            # print (dictitem['性别'])
            # 箱线图
            pathlist.append(item[3])
            hospital.append(dictitem['送检医院'])
            diagnosis.append(dictitem['病理诊断'])
            samplename.append(dictitem['样本编号'])
            stage.append(dictitem['分期'])
            medicine.append(dictitem['用药史'])
            datime.append(dictitem['送样日期'])
            msi.append(dictitem['MSI'])
            sex.append(dictitem['性别'])
            age.append(dictitem['年龄'])
            if dictitem['性别'] == '男':
                boy.append(dictitem['年龄'])
            if dictitem['性别'] == '女':
                girl.append(dictitem['年龄'])
        if (pathlist):
            myhospital = list(set(hospital))
            mydiagnosis = list(set(diagnosis))
            mystage = list(set(stage))
            mymedicine = list(set(medicine))
            mymsi = list(set(msi))
            #
            # 箱线图
            with open(r"/disk/linda/IgenomeCloudGemini/WordReport/TCGA11.txt", "r") as TCGA:
            # with open(r"/disk/lulu/TCGA11.txt", "r") as TCGA:
                temp = []
                cancerlist = []
                cancer = []
                for line in TCGA:
                    list1 = line.strip().split("\t")
                    temp = list1[0]
                    cancerlist.append(temp)
                cancer = sorted(set(cancerlist))
                # dict_medim={}
                # for cancertype in cancer:
                #     dict_medim[cancertype]=[]
                #     for line in TCGA:
                #         templist =line.strip().split("\t")
                #         if cancertype == templist[0]:
                #             dict_medim[cancertype].append(round(int(templist[2])/38),2)
                TCGAlist = []
                dict1 = {}
                tcgadict = {}
                dict_medim = {}
                for item in cancer:
                    # print (item)
                    dict1 = {item: []}
                    num = []
                    with open(r"/disk/linda/IgenomeCloudGemini/WordReport/TCGA11.txt", "r") as TCGA1:
                    # with open(r"/disk/lulu/TCGA11.txt", "r") as TCGA1:
                        for line in TCGA1:
                            list1 = line.strip().split("\t")
                            if item == list1[0]:
                                dict1[item].append(round(math.log10(int(list1[2]) / 38), 2))
                                num.append(round(math.log10(int(list1[2]) / 38), 2))
                    num.sort()
                    half = round(len(num) // 2, 2)
                    medim = round((num[half] + num[~half]) / 2, 2)
                    dict_medim[item] = medim
                    TCGAlist.append(dict1)
                    tcgadict.update(dict1)
            # print (dict_medim)
            geminilist = []
            num = []
            for key, item in enumerate(pathlist):
                filepath = "/home/zhangtao/gemini_clouds" + item +"T1.Somatic.WES.snv.simp.nor"
                # filepath="/home/zhangtao/gemini_clouds"+item+samplename[key]+".Somatic.WES.snv.simp.nor"
                # filepath = "/disk/lulu" + item + "T1.Somatic.WES.snv.simp.nor"

                with open(filepath, "r") as file:
                    num_change = 0
                    for line in file:
                        ge_list = line.strip().split("\t")
                        if ge_list[4] == "非同义替换":
                            num_change = num_change + 1
                    geminilist.append(round(math.log10(num_change / 35), 2))
                    num.append(round(math.log10(num_change / 35), 2))
            num.sort()
            half = round(len(num) // 2, 2)
            medim = round((num[half] + num[~half]) / 2, 2)
            dict_medim["gemini"] = medim
            dict1['gemini'] = geminilist
            tcgadict['gemini'] = geminilist
            TCGAlist.append(dict1['gemini'])
            # print(TCGAlist)
            # print (tcgadict)
            # print (dict_medim)
            # print (sorted(dict_medim.items(),key=lambda item:item[1]))
            finalTCGAlist = []
            for items in (sorted(dict_medim.items(), key=lambda item: item[1])):
                # print (items[0])
                dictl = {}
                for key, values in enumerate(tcgadict.items()):
                    if items[0] == values[0]:
                        dictl[values[0]] = values[1]
                        finalTCGAlist.append(dictl)
            # print (finalTCGAlist)

            dict['pancancer'] = finalTCGAlist

            countprovince = []
            position = 0
            realprovince = []
            for i in hospital:
                # csvFile1 = codecs.open("/disk/lulu/hospital.csv", "r", 'gbk')
                csvFile1 = codecs.open("/disk/linda/IgenomeCloudGemini/WordReport/hospital.csv", "r", 'gbk')
                reader1 = csv.DictReader(csvFile1)
                for row1 in reader1:
                    province = []
                    hospital = []
                    province.append(row1['所属省份'])
                    hospital.append(row1['医院名称'])
                    if i in row1['医院名称']:
                        position = hospital.index(row1['医院名称'])
                        # print (position)
                        realprovince = province[position]
                        countprovince.append(realprovince)
                        # print (realprovince)
                        # print (countprovince)
                        break

            provincelist = set(countprovince)
            tempprovincelist = []
            for item in provincelist:
                # print(item + "\t" + str(countprovince.count(item)))
                temp = {"name": item, "value": countprovince.count(item)}
                tempprovincelist.append(temp)
            dict["province"] = tempprovincelist
            # 按月统计样本量
            # for i in datime:
            #     j = i.strip().split('月')
            #     k = j[0].replace('年', '.')
            #     list1.append(k)
            # mylist1 = set(list1)
            # for item in sorted(mylist1):
            #     print(item + "\t" + str(list1.count(item)))

            # 按周统计样本量

            for i in datime:
                time = i.replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
                restime = datetime.strptime(time, '%Y-%m-%d').date()
                # d =restime+timedelta(days=7)
            week1 = ["2018年01月01日", '2018年01月02日', '2018年01月03日', '2018年01月04日', '2018年01月05日', '2018年01月06日',
                     '2018年01月07日']
            week2 = ["2018年01月08日", '2018年01月09日', '2018年01月10日', '2018年01月11日', '2018年01月12日', '2018年01月13日',
                     '2018年01月14日']
            week3 = ["2018年01月15日", '2018年01月16日', '2018年01月17日', '2018年01月18日', '2018年01月19日', '2018年01月20日',
                     '2018年01月21日']
            week4 = ["2018年01月22日", '2018年01月23日', '2018年01月24日', '2018年01月25日', '2018年01月26日', '2018年01月27日',
                     '2018年01月28日']
            week5 = ["2018年01月29日", '2018年01月30日', '2018年01月31日', '2018年02月01日', '2018年02月02日', '2018年02月03日',
                     '2018年02月04日']
            week6 = ["2018年02月05日", '2018年02月06日', '2018年02月07日', '2018年02月08日', '2018年02月09日', '2018年02月10日',
                     '2018年02月11日']
            week7 = ['2018年02月12日', "2018年02月13日", '2018年02月14日', '2018年02月15日', '2018年02月16日', '2018年02月17日',
                     '2018年02月18日']
            week8 = ['2018年02月19日', "2018年02月20日", '2018年02月21日', '2018年02月22日', '2018年02月23日', '2018年02月24日',
                     '2018年02月25日']
            week9 = ['2018年02月26日', "2018年02月27日", '2018年02月28日', '2018年03月01日', '2018年03月02日', '2018年03月03日',
                     '2018年03月04日']
            week10 = ['2018年03月05日', "2018年03月06日", '2018年03月07日', '2018年03月08日', '2018年03月09日', '2018年03月10日',
                      '2018年03月11日']
            week11 = ['2018年03月12日', "2018年03月13日", '2018年03月14日', '2018年03月15日', '2018年03月16日', '2018年03月17日',
                      '2018年03月18日']
            week12 = ['2018年03月19日', "2018年03月20日", '2018年03月21日', '2018年03月22日', '2018年03月23日', '2018年03月24日',
                      '2018年03月25日']
            week13 = ['2018年03月26日', "2018年03月27日", '2018年03月28日', '2018年03月29日', '2018年03月30日', '2018年03月31日',
                      '2018年04月01日']
            week14 = ['2018年04月02日', "2018年04月03日", '2018年04月04日', '2018年04月05日', '2018年04月06日', '2018年04月07日',
                      '2018年04月08日']
            week15 = ['2018年04月09日', "2018年04月10日", '2018年04月11日', '2018年04月12日', '2018年04月13日', '2018年04月14日',
                      '2018年04月15日']
            week16 = ['2018年04月16日', "2018年04月17日", '2018年04月18日', '2018年04月19日', '2018年04月20日', '2018年04月21日',
                      '2018年04月22日']
            week17 = ['2018年04月23日', "2018年04月24日", '2018年04月25日', '2018年04月26日', '2018年04月27日', '2018年04月28日',
                      '2018年04月29日']
            week18 = ['2018年04月30日', "2018年05月01日", '2018年05月02日', '2018年05月03日', '2018年05月04日', '2018年05月05日',
                      '2018年05月06日']
            week19 = ['2018年05月07日', "2018年05月08日", '2018年05月09日', '2018年05月10日', '2018年05月11日', '2018年05月12日',
                      '2018年05月13日']
            week20 = ['2018年05月14日', "2018年05月15日", '2018年05月16日', '2018年05月17日', '2018年05月18日', '2018年05月19日',
                      '2018年05月20日']
            week21 = ['2018年05月21日', "2018年05月22日", '2018年05月23日', '2018年05月24日', '2018年05月25日', '2018年05月26日',
                      '2018年05月27日']
            week22 = ['2018年05月28日', "2018年05月29日", '2018年05月30日', '2018年05月31日', '2018年06月01日']

            for i in datime:
                if i in week1:
                    list1.append(i)
                if i in week2:
                    list2.append(i)
                if i in week3:
                    list3.append(i)
                if i in week4:
                    list4.append(i)
                if i in week5:
                    list5.append(i)
                if i in week6:
                    list6.append(i)
                if i in week7:
                    list7.append(i)
                if i in week8:
                    list8.append(i)
                if i in week9:
                    list9.append(i)
                if i in week10:
                    list10.append(i)
                if i in week11:
                    list11.append(i)
                if i in week12:
                    list12.append(i)
                if i in week13:
                    list13.append(i)
                if i in week14:
                    list14.append(i)
                if i in week15:
                    list15.append(i)
                if i in week16:
                    list16.append(i)
                if i in week17:
                    list17.append(i)
                if i in week18:
                    list18.append(i)
                if i in week19:
                    list19.append(i)
                if i in week20:
                    list20.append(i)
                if i in week21:
                    list21.append(i)
                if i in week22:
                    list22.append(i)
            tempsamplelist = []
            count1 = len(list1)
            count2 = len(list2)
            count3 = len(list3)
            count4 = len(list4)
            count5 = len(list5)
            count6 = len(list6)
            count7 = len(list7)
            count8 = len(list8)
            count9 = len(list9)
            count10 = len(list10)
            count11 = len(list11)
            count12 = len(list12)
            count13 = len(list13)
            count14 = len(list14)
            count15 = len(list15)
            count16 = len(list16)
            count17 = len(list17)
            count18 = len(list18)
            count19 = len(list19)
            count20 = len(list20)
            count21 = len(list21)
            count22 = len(list22)
            tempsamplelist = [{"name": "week1", "value": count1}, {"name": "week2", "value": count2},
                              {"name": "week3", "value": count3}, {"name": "week4", "value": count4},
                              {"name": "week5", "value": count5}, {"name": "week6", "value": count6},
                              {"name": "week7", "value": count7}, {"name": "week8", "value": count8},
                              {"name": "week9", "value": count9}, {"name": "week10", "value": count10},
                              {"name": "week11", "value": count11},
                              {"name": "week12", "value": count12}, {"name": "week13", "value": count13},
                              {"name": "week14", "value": count14},
                              {"name": "week15", "value": count15}, {"name": "week16", "value": count16},
                              {"name": "week17", "value": count17},
                              {"name": "week18", "value": count18}, {"name": "week19", "value": count19},
                              {"name": "week20", "value": count20}, {"name": "week21", "value": count21},
                              {"name": "week22", "value": count22}]

            # mylis =list(set(list1))
            # for item in sorted(mylist1):
            #     print (item + "\t" + str(list1.count(item)))
            dict["sample_num"] = tempsamplelist

            # MSI
            tempmsilist = []
            for i in mymsi:
                temp = {"name": i, "value": msi.count(i)}
                tempmsilist.append(temp)
            dict["MSI"] = tempmsilist
            # print(json.dumps(dict))
            # print (i +"\t"+str(msi.count(i)))

            # diagnosis
            tempdiagnosislist = []
            for item in mydiagnosis:
                temp = {"name": item, "value": diagnosis.count(item)}
                tempdiagnosislist.append(temp)
            dict["diagnosis"] = tempdiagnosislist
            # print(item + "\t" + str(diagnosis.count(item)))
            # print(json.dumps(dict,ensure_ascii=False))

            # stage
            tempstagelist = []
            for i in mystage:
                temp = {"name": i, "value": stage.count(i)}
                tempstagelist.append(temp)
            dict["stage"] = tempstagelist

            # medicine
            tempmedicinelist = []
            for j in mymedicine:
                temp = {"name": j, "value": medicine.count(j)}
                tempmedicinelist.append(temp)
            dict["medicine"] = tempmedicinelist

            # sex、age
            tempsex_agelist = []
            # dict["sex_age"] = tempsex_agelist
            temp = {"[0,10)岁": {}, "[10,20)岁": {}, "[20,30)岁": {}, "[30,40)岁": {},
                    "[40,50)岁": {}, "[50,60)岁": {}, "[60,70)岁": {}, "[70,80)岁": {},
                    "[80,90)岁": {}, "[90,100)岁": {}}
            for i in boy:
                if 0 <= int(i) < 10:
                    num0 = num0 + 1

                if 10 <= int(i) < 20:
                    num01 = num01 + 1

                if 20 <= int(i) < 30:
                    num02 = num02 + 1

                if 30 <= int(i) < 40:
                    num1 = num1 + 1

                if 40 <= int(i) < 50:
                    num2 = num2 + 1
                if 50 <= int(i) < 60:
                    num3 = num3 + 1

                if 60 <= int(i) < 70:
                    num4 = num4 + 1

                if 70 <= int(i) < 80:
                    num5 = num5 + 1

                if 80 <= int(i) < 90:
                    num6 = num6 + 1

                if 90 <= int(i) < 100:
                    num7 = num7 + 1

            temp["[0,10)岁"]["男"] = num0
            temp["[10,20)岁"]["男"] = num01
            temp["[20,30)岁"]["男"] = num02
            temp["[30,40)岁"]["男"] = num1
            temp["[40,50)岁"]["男"] = num2
            temp["[50,60)岁"]["男"] = num3
            temp["[60,70)岁"]["男"] = num4
            temp["[70,80)岁"]["男"] = num5
            temp["[80,90)岁"]["男"] = num6
            temp["[90,100)岁"]["男"] = num7
            # print (temp)
            # print('男' + "\t" + "[0,10)" + "\t" + str(num0))
            # print('男' + "\t" + "[10,20)" + "\t" + str(num01))
            # print('男' + "\t" + "[20,30)" + "\t" + str(num02))
            # print('男' + "\t" + "[30,40)" + "\t" + str(num1))
            # print('男' + "\t" + "[40,50)" + "\t" + str(num2))
            # print('男' + "\t" + "[50,60)" + "\t" + str(num3))
            # print('男' + "\t" + "[60,70)" + "\t" + str(num4))
            # print('男' + "\t" + "[70,80)" + "\t" + str(num5))
            # print('男' + "\t" + "[80,90)" + "\t" + str(num6))
            # print('男' + "\t" + "[90,100)" + "\t" + str(num7))
            for i in girl:
                if 0 <= int(i) < 10:
                    num10 = num10 + 1
                if 10 <= int(i) < 20:
                    num101 = num101 + 1
                if 20 <= int(i) < 30:
                    num102 = num102 + 1
                if 30 <= int(i) < 40:
                    num11 = num11 + 1
                if 40 <= int(i) < 50:
                    num21 = num21 + 1
                if 50 <= int(i) < 60:
                    num31 = num31 + 1
                if 60 <= int(i) < 70:
                    num41 = num41 + 1
                if 70 <= int(i) < 80:
                    num51 = num51 + 1
                if 80 <= int(i) < 90:
                    num61 = num61 + 1
                if 90 <= int(i) < 100:
                    num71 = num71 + 1
            temp["[0,10)岁"]["女"] = num10
            temp["[10,20)岁"]["女"] = num101
            temp["[20,30)岁"]["女"] = num102
            temp["[30,40)岁"]["女"] = num11
            temp["[40,50)岁"]["女"] = num21
            temp["[50,60)岁"]["女"] = num31
            temp["[60,70)岁"]["女"] = num41
            temp["[70,80)岁"]["女"] = num51
            temp["[80,90)岁"]["女"] = num61
            temp["[90,100)岁"]["女"] = num71
            # print (temp)
            tempsex_agelist = [temp]
            dict["sex_age"] = tempsex_agelist
            # print (dict)

            # print (json.dumps(dict, ensure_ascii=False))
            return (json.dumps(dict, ensure_ascii=False))
        else:
            return ("None")

    else:
        # print ("test")
        # (sexvalue==['男','女'] or sexvalue==[]) and (agevalue==[] or agevalue==[0,125]) and (diagnosisvalue==[] or diagnosisvalue ==['非小细胞肺癌','小细胞肺癌','非鳞性非小细胞肺癌','肺鳞癌','肺腺癌','非腺鳞癌','大细胞癌']):
        dict = {}
        batchidlist = []
        basiclist = []
        sex = []
        age = []
        diagnosis = []
        stage = []
        medicine = []
        boy = []
        girl = []
        num0 = 0
        num01 = 0
        num02 = 0
        num10 = 0
        num101 = 0
        num102 = 0
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0
        num7 = 0
        num11 = 0
        num21 = 0
        num31 = 0
        num41 = 0
        num51 = 0
        num61 = 0
        num71 = 0
        datime = []
        diagnosis = []
        stage = []
        medicine = []
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        list7 = []
        list8 = []
        list9 = []
        list10 = []
        list11 = []
        list12 = []
        list13 = []
        list14 = []
        list15 = []
        list16 = []
        list17 = []
        list18 = []
        list19 = []
        list20 = []
        list21 = []
        list22 = []
        msi = []
        samplename = []
        # 箱线图
        pathlist = []

        hospital = []
        # print (rowlist)
        for item in rowlist:
            batchidlist.append(item[0])
            basiclist.append(item[1])
            dictitem = json.loads(item[1])

            # print (dictitem['年龄'],dictitem['性别'],dictitem['病理诊断'])
            if len(agevalue)==2:
                if ((sexvalue==[]) or (dictitem['性别'] in sexvalue) ) and ((agevalue==[]) or (int(dictitem['年龄']) in range(int(agevalue[0]),int(agevalue[1])+1)) or (dictitem['年龄'] in agevalue)) and ((diagnosisvalue==[]) or (dictitem['病理诊断'] in diagnosisvalue)):
                # if (dictitem['性别'] in sexvalue)and (int(dictitem['年龄']) in range(int(agevalue[0]),int(agevalue[1])+1)) :
                    # 箱线图
                    pathlist.append(item[3])
                    hospital.append(dictitem['送检医院'])
                    diagnosis.append(dictitem['病理诊断'])
                    samplename.append(dictitem['样本编号'])
                    stage.append(dictitem['分期'])
                    medicine.append(dictitem['用药史'])
                    datime.append(dictitem['送样日期'])
                    msi.append(dictitem['MSI'])
                    sex.append(dictitem['性别'])
                    age.append(dictitem['年龄'])
                    if dictitem['性别'] == '男':
                        boy.append(dictitem['年龄'])
                    if dictitem['性别'] == '女':
                        girl.append(dictitem['年龄'])
            else:
                if ((sexvalue==[]) or (dictitem['性别'] in sexvalue) ) and ((agevalue==[]) or (dictitem['年龄'] in agevalue)) and ((diagnosisvalue==[]) or (dictitem['病理诊断'] in diagnosisvalue)):
                # if (dictitem['性别'] in sexvalue)and (int(dictitem['年龄']) in range(int(agevalue[0]),int(agevalue[1])+1)) :
                    pathlist.append(item[3])
                    hospital.append(dictitem['送检医院'])
                    diagnosis.append(dictitem['病理诊断'])
                    samplename.append(dictitem['样本编号'])
                    stage.append(dictitem['分期'])
                    medicine.append(dictitem['用药史'])
                    datime.append(dictitem['送样日期'])
                    msi.append(dictitem['MSI'])
                    sex.append(dictitem['性别'])
                    age.append(dictitem['年龄'])
                    if dictitem['性别'] == '男':
                        boy.append(dictitem['年龄'])
                    if dictitem['性别'] == '女':
                        girl.append(dictitem['年龄'])
        #
        # print (sex)
        # print (age)
        # print (diagnosis)
        if (pathlist):
            myhospital = list(set(hospital))
            mydiagnosis = list(set(diagnosis))
            mystage = list(set(stage))
            mymedicine = list(set(medicine))
            mymsi = list(set(msi))
            #
            # 箱线图
            with open(r"/disk/linda/IgenomeCloudGemini/WordReport/TCGA11.txt", "r") as TCGA:
            # with open(r"/disk/lulu/TCGA11.txt", "r") as TCGA:
                temp = []
                cancerlist = []
                cancer = []
                for line in TCGA:
                    list1 = line.strip().split("\t")
                    temp = list1[0]
                    cancerlist.append(temp)
                cancer = sorted(set(cancerlist))
                # dict_medim={}
                # for cancertype in cancer:
                #     dict_medim[cancertype]=[]
                #     for line in TCGA:
                #         templist =line.strip().split("\t")
                #         if cancertype == templist[0]:
                #             dict_medim[cancertype].append(round(int(templist[2])/38),2)
                TCGAlist = []
                dict1 = {}
                tcgadict = {}
                dict_medim = {}
                for item in cancer:
                    # print (item)
                    dict1 = {item: []}
                    num = []
                    with open(r"/disk/linda/IgenomeCloudGemini/WordReport/TCGA11.txt", "r") as TCGA1:
                    # with open(r"/disk/lulu/TCGA11.txt", "r") as TCGA1:
                        for line in TCGA1:
                            list1 = line.strip().split("\t")
                            if item == list1[0]:
                                dict1[item].append(round(math.log10(int(list1[2]) / 38), 2))
                                num.append(round(math.log10(int(list1[2]) / 38), 2))
                    num.sort()

                    half = round(len(num) // 2, 2)
                    medim = round((num[half] + num[~half]) / 2, 2)
                    dict_medim[item] = medim
                    TCGAlist.append(dict1)
                    tcgadict.update(dict1)
            # print (dict_medim)
            geminilist = []
            num = []
            for key, item in enumerate(pathlist):
                filepath = "/home/zhangtao/gemini_clouds" + item +"T1.Somatic.WES.snv.simp.nor"
                # filepath="/home/zhangtao/gemini_clouds"+item+samplename[key]+".Somatic.WES.snv.simp.nor"
                # filepath = "/disk/lulu" + item + "T1.Somatic.WES.snv.simp.nor"

                with open(filepath, "r") as file:
                    num_change = 0
                    for line in file:
                        ge_list = line.strip().split("\t")
                        if ge_list[4] == "非同义替换":
                            num_change = num_change + 1
                    geminilist.append(round(math.log10(num_change / 35), 2))
                    num.append(round(math.log10(num_change / 35), 2))
            num.sort()
            half = round(len(num) // 2, 2)
            medim = round((num[half] + num[~half]) / 2, 2)
            dict_medim["gemini"] = medim
            dict1['gemini'] = geminilist
            tcgadict['gemini'] = geminilist
            TCGAlist.append(dict1['gemini'])
            # print(TCGAlist)
            # print (tcgadict)
            # print (dict_medim)
            # print (sorted(dict_medim.items(),key=lambda item:item[1]))
            finalTCGAlist = []
            for items in (sorted(dict_medim.items(), key=lambda item: item[1])):
                # print (items[0])
                dictl = {}
                for key, values in enumerate(tcgadict.items()):
                    if items[0] == values[0]:
                        dictl[values[0]] = values[1]
                        finalTCGAlist.append(dictl)
            # print (finalTCGAlist)

            dict['pancancer'] = finalTCGAlist
            #


            countprovince = []
            position = 0
            realprovince = []
            for i in hospital:
                # csvFile1 = codecs.open("/disk/lulu/hospital.csv", "r", 'gbk')
                csvFile1 = codecs.open("/disk/linda/IgenomeCloudGemini/WordReport/hospital.csv", "r", 'gbk')
                reader1 = csv.DictReader(csvFile1)
                for row1 in reader1:
                    province = []
                    hospital = []
                    province.append(row1['所属省份'])
                    hospital.append(row1['医院名称'])
                    if i in row1['医院名称']:
                        position = hospital.index(row1['医院名称'])
                        # print (position)
                        realprovince = province[position]
                        countprovince.append(realprovince)
                        # print (realprovince)
                        # print (countprovince)
                        break

            provincelist = set(countprovince)
            tempprovincelist = []
            for item in provincelist:
                # print(item + "\t" + str(countprovince.count(item)))
                temp = {"name": item, "value": countprovince.count(item)}
                tempprovincelist.append(temp)
            dict["province"] = tempprovincelist
            # 按月统计样本量
            # for i in datime:
            #     j = i.strip().split('月')
            #     k = j[0].replace('年', '.')
            #     list1.append(k)
            # mylist1 = set(list1)
            # for item in sorted(mylist1):
            #     print(item + "\t" + str(list1.count(item)))

            # 按周统计样本量

            for i in datime:
                time = i.replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
                restime = datetime.strptime(time, '%Y-%m-%d').date()
                # d =restime+timedelta(days=7)
            week1 = ["2018年01月01日", '2018年01月02日', '2018年01月03日', '2018年01月04日', '2018年01月05日', '2018年01月06日',
                     '2018年01月07日']
            week2 = ["2018年01月08日", '2018年01月09日', '2018年01月10日', '2018年01月11日', '2018年01月12日', '2018年01月13日',
                     '2018年01月14日']
            week3 = ["2018年01月15日", '2018年01月16日', '2018年01月17日', '2018年01月18日', '2018年01月19日', '2018年01月20日',
                     '2018年01月21日']
            week4 = ["2018年01月22日", '2018年01月23日', '2018年01月24日', '2018年01月25日', '2018年01月26日', '2018年01月27日',
                     '2018年01月28日']
            week5 = ["2018年01月29日", '2018年01月30日', '2018年01月31日', '2018年02月01日', '2018年02月02日', '2018年02月03日',
                     '2018年02月04日']
            week6 = ["2018年02月05日", '2018年02月06日', '2018年02月07日', '2018年02月08日', '2018年02月09日', '2018年02月10日',
                     '2018年02月11日']
            week7 = ['2018年02月12日', "2018年02月13日", '2018年02月14日', '2018年02月15日', '2018年02月16日', '2018年02月17日',
                     '2018年02月18日']
            week8 = ['2018年02月19日', "2018年02月20日", '2018年02月21日', '2018年02月22日', '2018年02月23日', '2018年02月24日',
                     '2018年02月25日']
            week9 = ['2018年02月26日', "2018年02月27日", '2018年02月28日', '2018年03月01日', '2018年03月02日', '2018年03月03日',
                     '2018年03月04日']
            week10 = ['2018年03月05日', "2018年03月06日", '2018年03月07日', '2018年03月08日', '2018年03月09日', '2018年03月10日',
                      '2018年03月11日']
            week11 = ['2018年03月12日', "2018年03月13日", '2018年03月14日', '2018年03月15日', '2018年03月16日', '2018年03月17日',
                      '2018年03月18日']
            week12 = ['2018年03月19日', "2018年03月20日", '2018年03月21日', '2018年03月22日', '2018年03月23日', '2018年03月24日',
                      '2018年03月25日']
            week13 = ['2018年03月26日', "2018年03月27日", '2018年03月28日', '2018年03月29日', '2018年03月30日', '2018年03月31日',
                      '2018年04月01日']
            week14 = ['2018年04月02日', "2018年04月03日", '2018年04月04日', '2018年04月05日', '2018年04月06日', '2018年04月07日',
                      '2018年04月08日']
            week15 = ['2018年04月09日', "2018年04月10日", '2018年04月11日', '2018年04月12日', '2018年04月13日', '2018年04月14日',
                      '2018年04月15日']
            week16 = ['2018年04月16日', "2018年04月17日", '2018年04月18日', '2018年04月19日', '2018年04月20日', '2018年04月21日',
                      '2018年04月22日']
            week17 = ['2018年04月23日', "2018年04月24日", '2018年04月25日', '2018年04月26日', '2018年04月27日', '2018年04月28日',
                      '2018年04月29日']
            week18 = ['2018年04月30日', "2018年05月01日", '2018年05月02日', '2018年05月03日', '2018年05月04日', '2018年05月05日',
                      '2018年05月06日']
            week19 = ['2018年05月07日', "2018年05月08日", '2018年05月09日', '2018年05月10日', '2018年05月11日', '2018年05月12日',
                      '2018年05月13日']
            week20 = ['2018年05月14日', "2018年05月15日", '2018年05月16日', '2018年05月17日', '2018年05月18日', '2018年05月19日',
                      '2018年05月20日']
            week21 = ['2018年05月21日', "2018年05月22日", '2018年05月23日', '2018年05月24日', '2018年05月25日', '2018年05月26日',
                      '2018年05月27日']
            week22 = ['2018年05月28日', "2018年05月29日", '2018年05月30日', '2018年05月31日', '2018年06月01日']

            for i in datime:
                if i in week1:
                    list1.append(i)
                if i in week2:
                    list2.append(i)
                if i in week3:
                    list3.append(i)
                if i in week4:
                    list4.append(i)
                if i in week5:
                    list5.append(i)
                if i in week6:
                    list6.append(i)
                if i in week7:
                    list7.append(i)
                if i in week8:
                    list8.append(i)
                if i in week9:
                    list9.append(i)
                if i in week10:
                    list10.append(i)
                if i in week11:
                    list11.append(i)
                if i in week12:
                    list12.append(i)
                if i in week13:
                    list13.append(i)
                if i in week14:
                    list14.append(i)
                if i in week15:
                    list15.append(i)
                if i in week16:
                    list16.append(i)
                if i in week17:
                    list17.append(i)
                if i in week18:
                    list18.append(i)
                if i in week19:
                    list19.append(i)
                if i in week20:
                    list20.append(i)
                if i in week21:
                    list21.append(i)
                if i in week22:
                    list22.append(i)
            tempsamplelist = []
            count1 = len(list1)
            count2 = len(list2)
            count3 = len(list3)
            count4 = len(list4)
            count5 = len(list5)
            count6 = len(list6)
            count7 = len(list7)
            count8 = len(list8)
            count9 = len(list9)
            count10 = len(list10)
            count11 = len(list11)
            count12 = len(list12)
            count13 = len(list13)
            count14 = len(list14)
            count15 = len(list15)
            count16 = len(list16)
            count17 = len(list17)
            count18 = len(list18)
            count19 = len(list19)
            count20 = len(list20)
            count21 = len(list21)
            count22 = len(list22)
            tempsamplelist = [{"name": "week1", "value": count1}, {"name": "week2", "value": count2},
                              {"name": "week3", "value": count3}, {"name": "week4", "value": count4},
                              {"name": "week5", "value": count5}, {"name": "week6", "value": count6},
                              {"name": "week7", "value": count7}, {"name": "week8", "value": count8},
                              {"name": "week9", "value": count9}, {"name": "week10", "value": count10},
                              {"name": "week11", "value": count11},
                              {"name": "week12", "value": count12}, {"name": "week13", "value": count13},
                              {"name": "week14", "value": count14},
                              {"name": "week15", "value": count15}, {"name": "week16", "value": count16},
                              {"name": "week17", "value": count17},
                              {"name": "week18", "value": count18}, {"name": "week19", "value": count19},
                              {"name": "week20", "value": count20}, {"name": "week21", "value": count21},
                              {"name": "week22", "value": count22}]

            # mylis =list(set(list1))
            # for item in sorted(mylist1):
            #     print (item + "\t" + str(list1.count(item)))
            dict["sample_num"] = tempsamplelist

            # MSI
            tempmsilist = []
            for i in mymsi:
                temp = {"name": i, "value": msi.count(i)}
                tempmsilist.append(temp)
            dict["MSI"] = tempmsilist
            # print(json.dumps(dict))
            # print (i +"\t"+str(msi.count(i)))

            # diagnosis
            tempdiagnosislist = []
            for item in mydiagnosis:
                temp = {"name": item, "value": diagnosis.count(item)}
                tempdiagnosislist.append(temp)
            dict["diagnosis"] = tempdiagnosislist
            # print(item + "\t" + str(diagnosis.count(item)))
            # print(json.dumps(dict,ensure_ascii=False))

            # stage
            tempstagelist = []
            for i in mystage:
                temp = {"name": i, "value": stage.count(i)}
                tempstagelist.append(temp)
            dict["stage"] = tempstagelist

            # medicine
            tempmedicinelist = []
            for j in mymedicine:
                temp = {"name": j, "value": medicine.count(j)}
                tempmedicinelist.append(temp)
            dict["medicine"] = tempmedicinelist

            # sex、age
            tempsex_agelist = []
            # dict["sex_age"] = tempsex_agelist
            temp = {"[0,10)岁": {}, "[10,20)岁": {}, "[20,30)岁": {}, "[30,40)岁": {},
                    "[40,50)岁": {}, "[50,60)岁": {}, "[60,70)岁": {}, "[70,80)岁": {},
                    "[80,90)岁": {}, "[90,100)岁": {}}
            for i in boy:
                if 0 <= int(i) < 10:
                    num0 = num0 + 1

                if 10 <= int(i) < 20:
                    num01 = num01 + 1

                if 20 <= int(i) < 30:
                    num02 = num02 + 1

                if 30 <= int(i) < 40:
                    num1 = num1 + 1

                if 40 <= int(i) < 50:
                    num2 = num2 + 1
                if 50 <= int(i) < 60:
                    num3 = num3 + 1

                if 60 <= int(i) < 70:
                    num4 = num4 + 1

                if 70 <= int(i) < 80:
                    num5 = num5 + 1

                if 80 <= int(i) < 90:
                    num6 = num6 + 1

                if 90 <= int(i) < 100:
                    num7 = num7 + 1

            temp["[0,10)岁"]["男"] = num0
            temp["[10,20)岁"]["男"] = num01
            temp["[20,30)岁"]["男"] = num02
            temp["[30,40)岁"]["男"] = num1
            temp["[40,50)岁"]["男"] = num2
            temp["[50,60)岁"]["男"] = num3
            temp["[60,70)岁"]["男"] = num4
            temp["[70,80)岁"]["男"] = num5
            temp["[80,90)岁"]["男"] = num6
            temp["[90,100)岁"]["男"] = num7
            # print (temp)
            # print('男' + "\t" + "[0,10)" + "\t" + str(num0))
            # print('男' + "\t" + "[10,20)" + "\t" + str(num01))
            # print('男' + "\t" + "[20,30)" + "\t" + str(num02))
            # print('男' + "\t" + "[30,40)" + "\t" + str(num1))
            # print('男' + "\t" + "[40,50)" + "\t" + str(num2))
            # print('男' + "\t" + "[50,60)" + "\t" + str(num3))
            # print('男' + "\t" + "[60,70)" + "\t" + str(num4))
            # print('男' + "\t" + "[70,80)" + "\t" + str(num5))
            # print('男' + "\t" + "[80,90)" + "\t" + str(num6))
            # print('男' + "\t" + "[90,100)" + "\t" + str(num7))
            for i in girl:
                if 0 <= int(i) < 10:
                    num10 = num10 + 1
                if 10 <= int(i) < 20:
                    num101 = num101 + 1
                if 20 <= int(i) < 30:
                    num102 = num102 + 1
                if 30 <= int(i) < 40:
                    num11 = num11 + 1
                if 40 <= int(i) < 50:
                    num21 = num21 + 1
                if 50 <= int(i) < 60:
                    num31 = num31 + 1
                if 60 <= int(i) < 70:
                    num41 = num41 + 1
                if 70 <= int(i) < 80:
                    num51 = num51 + 1
                if 80 <= int(i) < 90:
                    num61 = num61 + 1
                if 90 <= int(i) < 100:
                    num71 = num71 + 1
            temp["[0,10)岁"]["女"] = num10
            temp["[10,20)岁"]["女"] = num101
            temp["[20,30)岁"]["女"] = num102
            temp["[30,40)岁"]["女"] = num11
            temp["[40,50)岁"]["女"] = num21
            temp["[50,60)岁"]["女"] = num31
            temp["[60,70)岁"]["女"] = num41
            temp["[70,80)岁"]["女"] = num51
            temp["[80,90)岁"]["女"] = num61
            temp["[90,100)岁"]["女"] = num71
            # print (temp)
            tempsex_agelist = [temp]
            dict["sex_age"] = tempsex_agelist
                # print (dict)

                # print (json.dumps(dict, ensure_ascii=False))
            return (json.dumps(dict, ensure_ascii=False))
        else:
            return ("None")

########################
def forbatchonesql(begin_date):
    # print (type(begin_date))
    IP = '192.168.75.251'
    User_name = 'phpcms'
    password = 'yuanshi1985'
    database = 'gemini'
    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # select  *  from 数据表  where 时间字段名 BETWEEN '2016-02-01' AND '2016-02-05'  
    sql = "select s.batchid, s.basic_json, s.sample_data,t.outputfile from ge_task t inner join ge_sample s on t.sample_uniqueid = s.sample_uniqueid WHERE s.sample_data = 1 and date_format(s.commit_bat_time,'%%Y-%%m-%%d')='%s' " % (begin_date)
    # print (sql)
    # sql = "select batchid,basic_json from ge_sample WHERE sample_data=1 and commit_bat_time BETWEEN '%s' AND '%s'"%(begin_date,end_date)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        rowlist = []
        for row in results:
            rowlist.append(row)
    except:
        print("Error: unable to fetch data")
    db.close()
    # print (rowlist)
    return rowlist

def forbatchsql(begin_date,end_date):
    IP = '192.168.75.251'
    User_name = 'phpcms'
    password = 'yuanshi1985'
    database = 'gemini'
    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # select  *  from 数据表  where 时间字段名 BETWEEN '2016-02-01' AND '2016-02-05'  
    sql = "select s.batchid, s.basic_json, s.sample_data,t.outputfile from ge_task t inner join ge_sample s on t.sample_uniqueid = s.sample_uniqueid WHERE s.sample_data = 1 and s.commit_bat_time BETWEEN '%s' AND '%s'" % (begin_date,end_date)
    # sql = "select batchid,basic_json from ge_sample WHERE sample_data=1 and commit_bat_time BETWEEN '%s' AND '%s'"%(begin_date,end_date)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        rowlist = []
        for row in results:
            rowlist.append(row)
    except:
        print("Error: unable to fetch data")
    db.close()
    return rowlist
# 获取两个日期间的所有日期
# def getEveryDay(begin_date, end_date):
#     date_list = []
#     begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
#     end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
#     while begin_date <= end_date:
#         date_str = begin_date.strftime("%Y-%m-%d")
#         date_list.append(date_str)
#         begin_date += datetime.timedelta(days=1)
#     return date_list


##初始化为空或者全选时，输出所有的统计结果##
def fromsql():
    #从数据库中取出数据
    IP = '192.168.75.251'
    User_name = 'phpcms'
    password = 'yuanshi1985'
    database = 'gemini'
    db = MySQLdb.connect(host=IP, user=User_name, passwd=password, db=database, charset='utf8')
    cursor = db.cursor()
    # sql = "select batchid,basic_json,sample_data from ge_sample WHERE sample_data=1"
    sql = "select s.batchid, s.basic_json, s.sample_data, t.outputfile from ge_task t inner join ge_sample s on t.sample_uniqueid = s.sample_uniqueid WHERE s.sample_data = 1 "

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        rowlist = []
        for row in results:
            rowlist.append(row)
    except:
        print("Error: unable to fetch data")
    db.close()
    return rowlist

def all_display(rowlist):

    global dict
    dict = {}
    batchidlist=[]
    basiclist = []
    sex = []
    age = []
    diagnosis = []
    stage = []
    medicine = []
    boy = []
    girl = []
    num0=0
    num01=0
    num02=0
    num10=0
    num101=0
    num102=0
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0
    num7 = 0
    num11 = 0
    num21 = 0
    num31 = 0
    num41 = 0
    num51 = 0
    num61 = 0
    num71 = 0
    datime = []
    diagnosis =[]
    stage =[]
    medicine=[]
    list1 = []
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    list7=[]
    list8=[]
    list9=[]
    list10=[]
    list11=[]
    list12=[]
    list13=[]
    list14=[]
    list15=[]
    list16=[]
    list17=[]
    list18=[]
    list19=[]
    list20=[]
    list21=[]
    list22=[]
    msi =[]
    samplename = []
    # 箱线图
    pathlist = []
    hospital =[]
    for item in rowlist:
        # print (item[1])
        batchidlist.append(item[0])
        basiclist.append(item[1])
        # 箱线图
        pathlist.append(item[3])
        dictitem = json.loads(item[1])
        # print (dictitem['性别'])
        hospital.append(dictitem['送检医院'])
        diagnosis.append(dictitem['病理诊断'])
        samplename.append(dictitem['样本编号'])
        stage.append(dictitem['分期'])
        medicine.append(dictitem['用药史'])
        datime.append(dictitem['送样日期'])
        msi.append(dictitem['MSI'])
        sex.append(dictitem['性别'])
        age.append(dictitem['年龄'])
        if dictitem['性别'] == '男':
            boy.append(dictitem['年龄'])
        if dictitem['性别'] == '女':
            girl.append(dictitem['年龄'])
    if (pathlist):
        myhospital =list(set(hospital))
        mydiagnosis = list(set(diagnosis))
        mystage = list(set(stage))
        mymedicine = list(set(medicine))
        mymsi = list(set(msi))
        #
        # 箱线图
        with open(r"/disk/linda/IgenomeCloudGemini/WordReport/TCGA11.txt", "r") as TCGA:
        # with open(r"/disk/lulu/TCGA11.txt", "r") as TCGA:
            temp = []
            cancerlist = []
            cancer = []
            for line in TCGA:
                list1 = line.strip().split("\t")
                temp = list1[0]
                cancerlist.append(temp)
            cancer = sorted(set(cancerlist))
            # dict_medim={}
            # for cancertype in cancer:
            #     dict_medim[cancertype]=[]
            #     for line in TCGA:
            #         templist =line.strip().split("\t")
            #         if cancertype == templist[0]:
            #             dict_medim[cancertype].append(round(int(templist[2])/38),2)
            TCGAlist = []
            dict1 = {}
            tcgadict = {}
            dict_medim = {}
            for item in cancer:
                # print (item)
                dict1 = {item: []}
                num = []
                with open(r"/disk/linda/IgenomeCloudGemini/WordReport/TCGA11.txt", "r") as TCGA1:
                # with open(r"/disk/lulu/TCGA11.txt", "r") as TCGA1:
                    for line in TCGA1:
                        list1 = line.strip().split("\t")
                        if item == list1[0]:
                            dict1[item].append(round(math.log10(int(list1[2]) / 38), 2))
                            num.append(round(math.log10(int(list1[2]) / 38), 2))
                num.sort()
                half = round(len(num) // 2, 2)
                medim = round((num[half] + num[~half]) / 2, 2)
                dict_medim[item] = medim
                TCGAlist.append(dict1)
                tcgadict.update(dict1)
        # print (dict_medim)
        geminilist = []
        num = []
        for key, item in enumerate(pathlist):
            filepath = "/home/zhangtao/gemini_clouds" + item + "T1.Somatic.WES.snv.simp.nor"
            # filepath="/home/zhangtao/gemini_clouds"+item+samplename[key]+".Somatic.WES.snv.simp.nor"
            # filepath = "/disk/lulu" + item + "T1.Somatic.WES.snv.simp.nor"

            with open(filepath, "r") as file:
                num_change = 0
                for line in file:
                    ge_list = line.strip().split("\t")
                    if ge_list[4] == "非同义替换":
                        num_change = num_change + 1
                geminilist.append(round(math.log10(num_change / 35), 2))
                num.append(round(math.log10(num_change / 35), 2))
        num.sort()
        half = round(len(num) // 2, 2)
        medim = round((num[half] + num[~half]) / 2, 2)
        dict_medim["gemini"] = medim
        dict1['gemini'] = geminilist
        tcgadict['gemini'] = geminilist
        TCGAlist.append(dict1['gemini'])
        # print(TCGAlist)
        # print (tcgadict)
        # print (dict_medim)
        # print (sorted(dict_medim.items(),key=lambda item:item[1]))
        finalTCGAlist = []
        for items in (sorted(dict_medim.items(), key=lambda item: item[1])):
            # print (items[0])
            dictl = {}
            for key, values in enumerate(tcgadict.items()):
                if items[0] == values[0]:
                    dictl[values[0]] = values[1]
                    finalTCGAlist.append(dictl)
        # print (finalTCGAlist)

        dict['pancancer'] = finalTCGAlist
        #

        countprovince = []
        position = 0
        realprovince = []
        for i in hospital:
            csvFile1 = codecs.open("/disk/linda/IgenomeCloudGemini/WordReport/hospital.csv", "r", 'gbk')
            # csvFile1 = codecs.open("/disk/lulu/hospital.csv", "r", 'gbk')
            reader1 = csv.DictReader(csvFile1)
            for row1 in reader1:
                province = []
                hospital = []
                province.append(row1['所属省份'])
                hospital.append(row1['医院名称'])
                if i in row1['医院名称']:
                    position = hospital.index(row1['医院名称'])
                    # print (position)
                    realprovince = province[position]
                    countprovince.append(realprovince)
                    # print (realprovince)
                    # print (countprovince)
                    break

        provincelist = set(countprovince)
        tempprovincelist=[]
        for item in provincelist:
            # print(item + "\t" + str(countprovince.count(item)))
            temp = {"name": item, "value": countprovince.count(item)}
            tempprovincelist.append(temp)
        dict["province"] = tempprovincelist
        #按月统计样本量
        # for i in datime:
        #     j = i.strip().split('月')
        #     k = j[0].replace('年', '.')
        #     list1.append(k)
        # mylist1 = set(list1)
        # for item in sorted(mylist1):
        #     print(item + "\t" + str(list1.count(item)))

        #按周统计样本量

        for i in datime:
            time =i.replace(r'年','-').replace(r'月','-').replace(r'日','')
            # print (time)
            restime = datetime.strptime(time,'%Y-%m-%d').date()
            # d =restime+timedelta(days=7)
        week1 =["2018年01月01日",'2018年01月02日','2018年01月03日','2018年01月04日','2018年01月05日','2018年01月06日','2018年01月07日']
        week2 = ["2018年01月08日", '2018年01月09日', '2018年01月10日', '2018年01月11日', '2018年01月12日', '2018年01月13日', '2018年01月14日']
        week3 = ["2018年01月15日", '2018年01月16日', '2018年01月17日', '2018年01月18日', '2018年01月19日', '2018年01月20日', '2018年01月21日']
        week4 = ["2018年01月22日", '2018年01月23日', '2018年01月24日', '2018年01月25日', '2018年01月26日', '2018年01月27日', '2018年01月28日']
        week5 = ["2018年01月29日", '2018年01月30日', '2018年01月31日', '2018年02月01日', '2018年02月02日', '2018年02月03日', '2018年02月04日']
        week6 = ["2018年02月05日", '2018年02月06日', '2018年02月07日', '2018年02月08日', '2018年02月09日', '2018年02月10日', '2018年02月11日']
        week7 = ['2018年02月12日',"2018年02月13日", '2018年02月14日', '2018年02月15日', '2018年02月16日', '2018年02月17日', '2018年02月18日']
        week8 = ['2018年02月19日',"2018年02月20日", '2018年02月21日', '2018年02月22日', '2018年02月23日', '2018年02月24日', '2018年02月25日']
        week9 = ['2018年02月26日',"2018年02月27日", '2018年02月28日', '2018年03月01日', '2018年03月02日', '2018年03月03日', '2018年03月04日']
        week10 = ['2018年03月05日',"2018年03月06日", '2018年03月07日', '2018年03月08日', '2018年03月09日', '2018年03月10日', '2018年03月11日']
        week11 = ['2018年03月12日',"2018年03月13日", '2018年03月14日', '2018年03月15日', '2018年03月16日', '2018年03月17日', '2018年03月18日']
        week12 =['2018年03月19日',"2018年03月20日", '2018年03月21日', '2018年03月22日', '2018年03月23日', '2018年03月24日', '2018年03月25日']
        week13=['2018年03月26日',"2018年03月27日", '2018年03月28日', '2018年03月29日', '2018年03月30日', '2018年03月31日', '2018年04月01日']
        week14 =['2018年04月02日',"2018年04月03日", '2018年04月04日', '2018年04月05日', '2018年04月06日', '2018年04月07日', '2018年04月08日']
        week15=['2018年04月09日',"2018年04月10日", '2018年04月11日', '2018年04月12日', '2018年04月13日', '2018年04月14日', '2018年04月15日']
        week16=['2018年04月16日',"2018年04月17日", '2018年04月18日', '2018年04月19日', '2018年04月20日', '2018年04月21日', '2018年04月22日']
        week17=['2018年04月23日',"2018年04月24日", '2018年04月25日', '2018年04月26日', '2018年04月27日', '2018年04月28日', '2018年04月29日']
        week18=[ '2018年04月30日',"2018年05月01日", '2018年05月02日', '2018年05月03日', '2018年05月04日', '2018年05月05日', '2018年05月06日']
        week19 =['2018年05月07日',"2018年05月08日", '2018年05月09日', '2018年05月10日', '2018年05月11日', '2018年05月12日', '2018年05月13日']
        week20=['2018年05月14日',"2018年05月15日", '2018年05月16日', '2018年05月17日', '2018年05月18日', '2018年05月19日', '2018年05月20日']
        week21=['2018年05月21日',"2018年05月22日", '2018年05月23日', '2018年05月24日', '2018年05月25日', '2018年05月26日', '2018年05月27日']
        week22=['2018年05月28日',"2018年05月29日", '2018年05月30日', '2018年05月31日', '2018年06月01日']

        for i in datime:
            if i in week1:
                list1.append(i)
            if i in week2:
                list2.append(i)
            if i in week3:
                list3.append(i)
            if i in week4:
                list4.append(i)
            if i in week5:
                list5.append(i)
            if i in week6:
                list6.append(i)
            if i in week7:
                list7.append(i)
            if i in week8:
                list8.append(i)
            if i in week9:
                list9.append(i)
            if i in week10:
                list10.append(i)
            if i in week11:
                list11.append(i)
            if i in week12:
                list12.append(i)
            if i in week13:
                list13.append(i)
            if i in week14:
                list14.append(i)
            if i in week15:
                list15.append(i)
            if i in week16:
                list16.append(i)
            if i in week17:
                list17.append(i)
            if i in week18:
                list18.append(i)
            if i in week19:
                list19.append(i)
            if i in week20:
                list20.append(i)
            if i in week21:
                list21.append(i)
            if i in week22:
                list22.append(i)
        tempsamplelist=[]
        count1 =len(list1)
        count2 =len(list2)
        count3 =len(list3)
        count4 =len(list4)
        count5 = len(list5)
        count6 = len(list6)
        count7 = len(list7)
        count8 = len(list8)
        count9 = len(list9)
        count10 = len(list10)
        count11 = len(list11)
        count12 = len(list12)
        count13 = len(list13)
        count14 = len(list14)
        count15 = len(list15)
        count16 = len(list16)
        count17 = len(list17)
        count18 = len(list18)
        count19 = len(list19)
        count20 = len(list20)
        count21 = len(list21)
        count22 = len(list22)
        tempsamplelist=[{"name": "week1", "value": count1},{"name":"week2","value":count2},
                        {"name":"week3","value":count3},{"name":"week4","value":count4},
                        {"name":"week5","value":count5},{"name":"week6","value":count6},
                        {"name":"week7","value":count7},{"name":"week8","value":count8},
                        {"name":"week9","value":count9},{"name":"week10","value":count10},{"name":"week11","value":count11},
                        {"name":"week12","value":count12},{"name":"week13","value":count13},{"name":"week14","value":count14},
                        {"name":"week15","value":count15},{"name":"week16","value":count16},{"name":"week17","value":count17},
                        {"name":"week18","value":count18},{"name":"week19","value":count19},{"name":"week20","value":count20},{"name":"week21","value":count21},
                        {"name":"week22","value":count22}]

        # mylis =list(set(list1))
        # for item in sorted(mylist1):
        #     print (item + "\t" + str(list1.count(item)))
        dict["sample_num"]=tempsamplelist

        #MSI
        tempmsilist=[]
        for i in mymsi:
            temp = {"name":i,"value":msi.count(i)}
            tempmsilist.append(temp)
        dict["MSI"]=tempmsilist
        # print(json.dumps(dict))
            # print (i +"\t"+str(msi.count(i)))

        #diagnosis
        tempdiagnosislist=[]
        for item in mydiagnosis:
            temp = {"name":item,"value":diagnosis.count(item)}
            tempdiagnosislist.append(temp)
        dict["diagnosis"]=tempdiagnosislist
            # print(item + "\t" + str(diagnosis.count(item)))
        # print(json.dumps(dict,ensure_ascii=False))

        #stage
        tempstagelist=[]
        for i in mystage:
            temp ={"name":i,"value":stage.count(i)}
            tempstagelist.append(temp)
        dict["stage"]=tempstagelist

        #medicine
        tempmedicinelist=[]
        for j in mymedicine:
            temp ={"name":j,"value":medicine.count(j)}
            tempmedicinelist.append(temp)
        dict["medicine"]=tempmedicinelist

        #sex、age
        tempsex_agelist=[]
        # dict["sex_age"] = tempsex_agelist
        temp= {"[0,10)岁": {},"[10,20)岁":{},"[20,30)岁":{},"[30,40)岁":{},
               "[40,50)岁":{},"[50,60)岁":{},"[60,70)岁":{},"[70,80)岁":{},
               "[80,90)岁":{},"[90,100)岁":{}}
        for i in boy:
            if 0 <=int(i) < 10:
                num0 =num0 + 1

            if 10 <=int(i) < 20:
                num01 =num01 + 1

            if 20 <= int(i) < 30:
                num02 = num02 +1

            if 30 <= int(i) < 40:
                num1 = num1 + 1

            if 40 <= int(i) < 50:
                num2 = num2 + 1
            if 50 <= int(i) < 60:
                num3 = num3 + 1

            if 60 <= int(i) < 70:
                num4 = num4 + 1

            if 70 <= int(i) < 80:
                num5 = num5 + 1

            if 80 <= int(i) < 90:
                num6 = num6 + 1

            if 90 <= int(i) < 100:
                num7 = num7 + 1

        temp["[0,10)岁"]["男"]=num0
        temp["[10,20)岁"]["男"]=num01
        temp["[20,30)岁"]["男"]=num02
        temp["[30,40)岁"]["男"]=num1
        temp["[40,50)岁"]["男"]=num2
        temp["[50,60)岁"]["男"]=num3
        temp["[60,70)岁"]["男"]=num4
        temp["[70,80)岁"]["男"]=num5
        temp["[80,90)岁"]["男"]=num6
        temp["[90,100)岁"]["男"]=num7
        # print (temp)
        # print('男' + "\t" + "[0,10)" + "\t" + str(num0))
        # print('男' + "\t" + "[10,20)" + "\t" + str(num01))
        # print('男' + "\t" + "[20,30)" + "\t" + str(num02))
        # print('男' + "\t" + "[30,40)" + "\t" + str(num1))
        # print('男' + "\t" + "[40,50)" + "\t" + str(num2))
        # print('男' + "\t" + "[50,60)" + "\t" + str(num3))
        # print('男' + "\t" + "[60,70)" + "\t" + str(num4))
        # print('男' + "\t" + "[70,80)" + "\t" + str(num5))
        # print('男' + "\t" + "[80,90)" + "\t" + str(num6))
        # print('男' + "\t" + "[90,100)" + "\t" + str(num7))
        for i in girl:
            if 0 <=int(i) < 10:
                num10 =num10 + 1
            if 10 <=int(i) < 20:
                num101 =num101 + 1
            if 20 <= int(i) < 30:
                num102 = num102 + 1
            if 30 <= int(i) < 40:
                num11 = num11 + 1
            if 40 <= int(i) < 50:
                num21 = num21 + 1
            if 50 <= int(i) < 60:
                num31 = num31 + 1
            if 60 <= int(i) < 70:
                num41 = num41 + 1
            if 70 <= int(i) < 80:
                num51 = num51 + 1
            if 80 <= int(i) < 90:
                num61 = num61 + 1
            if 90 <= int(i) < 100:
                num71 = num71 + 1
        temp["[0,10)岁"]["女"]=num10
        temp["[10,20)岁"]["女"]=num101
        temp["[20,30)岁"]["女"]=num102
        temp["[30,40)岁"]["女"]=num11
        temp["[40,50)岁"]["女"]=num21
        temp["[50,60)岁"]["女"]=num31
        temp["[60,70)岁"]["女"]=num41
        temp["[70,80)岁"]["女"]=num51
        temp["[80,90)岁"]["女"]=num61
        temp["[90,100)岁"]["女"]=num71
        # print (temp)
        tempsex_agelist=[temp]
        dict["sex_age"] = tempsex_agelist
        # print (dict)

        # print (json.dumps(dict, ensure_ascii=False))
        return (json.dumps(dict, ensure_ascii=False))
    else:
        return ("None")

# # #
# if __name__ == '__main__':
#     # data = {"性别": [], "年龄": [], "病理诊断": [], "病人批次": {"min":"2018-01-08","max":"2018-02-24"}}
#     data = {"性别": [], "年龄": [], "病理诊断": [], "病人批次": {"min": "2018-01-08", "max": 0}}
#     # data = {"性别": [], "年龄": [], "病理诊断": ["腺鳞癌"], "病人批次": []}
#     # data = {"性别": ["男"], "年龄": ["65"], "病理诊断": [], "病人批次": ["2018-01-01","2018-01-10"]}
#     # data= {"性别": [], "年龄": [], "病理诊断": [], "病人批次": []}
#     # data = {"性别": [], "年龄": [], "病理诊断": [], "病人批次": ["2018-01-01", "2018-01-10"]}
#     label_result(data)