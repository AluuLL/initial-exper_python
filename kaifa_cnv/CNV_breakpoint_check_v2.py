#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam
#called CNV region adjust
'''断点区域校正
    删掉没有pair_reads支持信号的CBS区域'''




class FileIter():
    context = {}
    def __init__(self, fileName):
        try:
            self.file = open(fileName, 'r')

        except IOError as E:
            self.ERROR = True
            print ("Can't open %s!" % (fileName))
            print (E)


    def next(self):
        line = self.file.readline()
        if line == '':
            raise StopIteration
        else:
            return line.strip('\n').split('\t')


    def __iter__(self):
        return self

def search_R_break(inputItem):
    value =0 #为了计算均值使用
    reads_count=0
    pair_position=[]
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    if (int(inputItem[2]) - int(longth) >= 0) and (int(inputItem[3]) - int(longth)) >= 0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[2]) - int(longth), int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                # print read.reference_start
                # print range(int(inputItem[2])-int(longth),int(inputItem[2])+int(longth)+1)
                if read.reference_start in range(int(inputItem[2])-int(longth),int(inputItem[2])+int(longth)+1):
                    pair_position.append(read.next_reference_start)
    elif int(inputItem[2]) - int(longth) < 0:
        for read in bamfile.fetch(inputItem[1], 0, int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                if read.reference_start in range(0,int(inputItem[2])+int(longth)+1):
                    pair_position.append(read.next_reference_start)
    list=sorted(pair_position)
    listprint = []#目标扎堆列表
    listlinshi=[]#临时列表
    listnoise=[]#噪音列表，即是pair reads的位置小于CBS区域的起始位置
    flag = 0 #flag为1表示，进入下个扎堆判断
    # print "1"
    for i in list:
        if i > int(inputItem[2]):#判断pair reads的位置是否在起始位置之前，若不是则进入该条件；若是则表示是噪音信号执行else；
            if listprint:
                if flag == 0:
                    if i-listprint[0] <= 1000:
                        listprint.append(i)
                    else:
                        flag = 1
                        listlinshi=[]
                        listlinshi.append(i)
                        # count =1

                else:
                    if i -listlinshi[0]<=1000:
                        listlinshi.append(i)
                    else:
                        flag = 0
                        if len(listprint)<len(listlinshi):
                            listprint=listlinshi
                        else:
                            listlinshi=[]
            else:
                listprint.append(i)
        else:
            listnoise.append(i)

    # print list
    # print listprint
    # print listnoise
    # print inputItem
    for i in listprint:
        value=value+i
    if len(listprint)>0:
        inputItem[3]=str(value/len(listprint))
    count_noise=len(listnoise)
    # inputItem.append(str(count_noise))
    # print inputItem
    return inputItem


def search_L_break(inputItem):
    value =0 #为了计算均值使用
    reads_count=0
    pair_position=[]
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    if (int(inputItem[2]) - int(longth) >= 0) and (int(inputItem[3]) - int(longth)) >= 0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[3]) - int(longth), int(inputItem[3]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                if read.reference_start in range(int(inputItem[3])-int(longth),int(inputItem[3])+int(longth)+1):
                    pair_position.append(read.next_reference_start)
    elif (int(inputItem[3]) - int(longth)) < 0:
        for read in bamfile.fetch(inputItem[1],0, int(inputItem[3]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                if read.reference_start in range(0,int(inputItem[3])+int(longth)+1):
                    pair_position.append(read.next_reference_start)
    list=sorted(pair_position)
    listprint = []#目标扎堆列表
    listlinshi=[]#临时列表
    listnoise=[]#噪音列表，即是pair reads的位置大于CBS区域的终止位置
    flag = 0 #flag为1表示，进入下个扎堆判断
    # print "2"
    for i in list:
        if i  < int(inputItem[3]):#判断pair reads的位置是否在终止位置之后，若不是则进入该条件；若是则表示是噪音信号执行else；
            if listprint:
                # num = num + 1
                if flag == 0:
                    if i-listprint[0] <= 1000:
                        listprint.append(i)
                    else:
                        flag = 1
                        listlinshi=[]
                        listlinshi.append(i)
                        # count =1

                else:
                    if i -listlinshi[0]<=1000:
                        # count= count+ 1
                        listlinshi.append(i)
                    else:
                        flag = 0
                        if len(listprint)<len(listlinshi):
                            listprint=listlinshi
                        else:
                            listlinshi=[]
            else:
                listprint.append(i)
        else:
            listnoise.append(i)

    # print list
    # print listprint
    # print listnoise
    # print inputItem
    for i in listprint:
        value=value+i
    if len(listprint)>0:
        inputItem[2]=str(value/len(listprint))
    count_noise=len(listnoise)
    # inputItem.append(str(count_noise))
    # print inputItem
    return inputItem

def search_L_R_break(inputItem):
    value = 0  # 为了计算左断点均值使用
    value1 =0  # 为了计算右断点均值使用
    reads_count = 0
    reads_position=[]
    pair_position = []
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    if (int(inputItem[2]) - int(longth) >= 0) and (int(inputItem[3]) - int(longth)) >= 0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[2]),int(inputItem[3])):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                reads_count = reads_count + 1
                reads_position.append(read.reference_start)
                pair_position.append(read.next_reference_start)
    list = sorted(reads_position)
    if len(list)>0:
        listprint = []  # 目标扎堆列表
        listlinshi = []  # 临时列表
        listnoise = []  # 噪音列表，即是pair reads的位置大于CBS区域的终止位置小于CBS区域的起始位置
        flag = 0  # flag为1表示，进入下个扎堆判断
        for i in list:
            if i < int(inputItem[3]) and i > int(inputItem[2]):  # 判断pair reads的位置是否在终止位置之后起始位置之前，若不是则进入该条件；若是则表示是噪音信号执行else；
                if listprint:
                    # num = num + 1
                    if flag == 0:
                        if i - listprint[0] <= 1000:
                            listprint.append(i)
                        else:
                            flag = 1
                            listlinshi = []
                            listlinshi.append(i)
                            # count =1

                    else:
                        if i - listlinshi[0] <= 1000:
                            # count= count+ 1
                            listlinshi.append(i)
                        else:
                            flag = 0
                            if len(listprint) < len(listlinshi):
                                listprint = listlinshi
                            else:
                                listlinshi = []
                else:
                    listprint.append(i)
            else:
                listnoise.append(i)
        for i in listprint:
            value = value + i
        if len(listprint)>0:
            inputItem[2] = str(value / len(listprint))

    list1 = sorted(pair_position)
    if len(list1) > 0:
        listprint = []  # 目标扎堆列表
        listlinshi = []  # 临时列表
        flag = 0  # flag为1表示，进入下个扎堆判断
        for i in list1:
            if i > int(inputItem[2]):  # 判断pair reads的位置是否在终止位置之后起始位置之前，若不是则进入该条件；若是则表示是噪音信号执行else；
                if listprint:
                    # num = num + 1
                    if flag == 0:
                        if i - listprint[0] <= 1000:
                            listprint.append(i)
                        else:
                            flag = 1
                            listlinshi = []
                            listlinshi.append(i)
                            # count =1

                    else:
                        if i - listlinshi[0] <= 1000:
                            # count= count+ 1
                            listlinshi.append(i)
                        else:
                            flag = 0
                            if len(listprint) < len(listlinshi):
                                listprint = listlinshi
                            else:
                                listlinshi = []
                else:
                    listprint.append(i)
            else:
                listnoise.append(i)
        for i in listprint:
            value1 = value1 + i
        if len(listprint) > 0:
            inputItem[3] = str(value1 / len(listprint))

    return inputItem

def count_bp(inputItem):
    global inputFileBAMName
    global distance
    global longth
    realinputItem=[]
    L_reads_count=0
    L_pair_reads_count=0
    R_reads_count=0
    R_pair_reads_count=0
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    if int(inputItem[2])-int(longth) >=0 and  int(inputItem[3])-int(longth) >=0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[2]) - int(longth), int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                # print read
                # print abs(read.template_length)
                # print read.reference_id,read.next_reference_id
                # print read.reference_start,read.next_reference_start
                L_reads_count=L_reads_count+1
                if read.next_reference_start >= (int(inputItem[3]) - int(longth)) and read.next_reference_start <= (int(inputItem[3]) + int(longth)):
                    L_pair_reads_count=L_pair_reads_count+1
    elif int(inputItem[2])-int(longth) < 0 and  (int(inputItem[3])-int(longth)) >=0:
        for read in bamfile.fetch(inputItem[1], 0, int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                L_reads_count=L_reads_count+1
                if read.next_reference_start >= (int(inputItem[3]) - int(longth)) and read.next_reference_start <= (int(inputItem[3]) + int(longth)):
                    L_pair_reads_count=L_pair_reads_count+1
    elif int(inputItem[2])-int(longth) < 0 and  (int(inputItem[3])-int(longth)) < 0:
        for read in bamfile.fetch(inputItem[1], 0, int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                continue
            else:
                L_reads_count=L_reads_count+1
                if read.next_reference_start >= 0 and read.next_reference_start <= (int(inputItem[3]) + int(longth)):
                    L_pair_reads_count=L_pair_reads_count+1

    if L_reads_count>=3:
        if L_pair_reads_count < 3:
            realinputItem=search_R_break(inputItem)
        else:
            realinputItem=inputItem
    if 0 < L_reads_count<3:
        if (int(inputItem[2]) - int(longth) >= 0) and (int(inputItem[3]) - int(longth)) >= 0:
            for read in bamfile.fetch(inputItem[1], int(inputItem[3]) - int(longth), int(inputItem[3]) + int(longth)):
                if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                    continue
                else:

                    R_reads_count = R_reads_count + 1
                    if read.next_reference_start >= (int(inputItem[2]) - int(longth)) and read.next_reference_start <= (int(inputItem[2]) + int(longth)):
                        R_pair_reads_count = R_pair_reads_count + 1
        elif (int(inputItem[2]) - int(longth) < 0) and (int(inputItem[3]) - int(longth)) >= 0:
            for read in bamfile.fetch(inputItem[1],int(inputItem[3]) - int(longth),int(inputItem[3]) + int(longth)):
                if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                    continue
                else:
                    R_reads_count = R_reads_count + 1
                    if read.next_reference_start >= 0 and read.next_reference_start <= (int(inputItem[2]) + int(longth)):
                        R_pair_reads_count = R_pair_reads_count + 1
        elif (int(inputItem[2]) - int(longth) <0) and (int(inputItem[3]) - int(longth)) < 0:
            for read in bamfile.fetch(inputItem[1], 0, int(inputItem[3]) + int(longth)):
                if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id:
                    continue
                else:

                    R_reads_count = R_reads_count + 1
                    if read.next_reference_start >= 0 and read.next_reference_start <= (int(inputItem[2]) + int(longth)):
                        R_pair_reads_count = R_pair_reads_count + 1
        if R_reads_count >= 3:
            realinputItem=search_L_break(inputItem)

        if 0<R_reads_count < 3:
            realinputItem=search_L_R_break(inputItem)
        # if L_reads_count==0 and R_reads_count==0:
        #     print "1"
    # print realinputItem

    return realinputItem


def a(x):
    print (x)
class allCallerSimple():
    def __init__(self, **kwargs):
        self.kwargs = kwargs



    def run(self):
        global inputFileBAMName
        global distance
        global longth
        inputFileCBSName = self.kwargs.get('inputFileCBSName')
        inputFileBAMName = self.kwargs.get('inputFileBAMName')
        distance = self.kwargs.get('distance')
        outputFileName = self.kwargs.get('outputFileName')
        longth = self.kwargs.get('longth')
        ##
        try:
            F = open(outputFileName, 'w')
        except IOError:
            print ('IO error: %s' % (outputFileName))
            sys.exit(-1)

        inputCBSInst = FileIter(inputFileCBSName)
        # with concurrent.futures.ProcessPoolExecutor() as executor :
        #     for inputItem in inputCBSInst:
        with concurrent.futures.ProcessPoolExecutor(max_workers=15) as executor :
            line = executor.map(count_bp,inputCBSInst)
        # line = map(lambda x:count_bp(x),inputCBSInst)
        for item in line:
            if len(item)!=0:
                print item
                F.write('\t'.join(item) +'\n')
        F.close()



def param(argv):
    global inputfile_CBS
    global inputfile_BAM
    global outputfile
    global dis
    global long

    try:
        options, args = getopt.getopt(argv, "hi:b:o:d:l:",
                                      ["help", "inputCBS=", "inputBAM=","output=", "dis=","long="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for option, value in options:
        if not option:
            usage()
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        if option in ("-i", "--inputCBS"):
            inputfile_CBS = value
        if option in ("-o", "--output"):
            outputfile = value
        if option in ("-d", "--dis"):
            dis = value
        if option in ("-b", "--inputBAM"):
            inputfile_BAM = value
        if option in ("-l", "--long"):
            long = value

            # print (options,args)
    if args:
        print ("error arrgs:%s .please input --help to get the usage" % args)


def usage():
    print ('''
      This program can complish CBS file's surrounding depth caculate function.
      Options include:
        -i(--inputCBS=) input .CBS file                    :inputCBSfile 
        -b(--inputBAM=) input .bam file                    :input_file's chr &star&end column from 0 
        -o(--output=) outputfile                           :output_file 
        -d(--dis=)                                         :L_COV& R_COV span,fault is 1k
        -l(--long=)                                        :cbs tolerant paired reads region span ,faulut is 500bp
        ''')


def cmdDict():
    global inputfile_CBS
    global inputfile_BAM
    global outputfile
    global dis
    global long
    # global percent
    # global site
    # sitestr = site.strip().split(",")
    callerDict = {
        'inputFileCBSName': inputfile_CBS,
        'inputFileBAMName': inputfile_BAM,
        'outputFileName': outputfile,
        'distance': dis,
        'longth':long
    }

    return callerDict


if __name__ == '__main__':
    inputfile_CBS = "" #输入待求的CBS文件
    inputfile_BAM = "" #输入对应该CBS文件的cov文件
    outputfile = ""    #输出文件名
    dis = 1000           #前后surrounding的大小,默认1k
    long = 500          #cbs区域左右pair对容忍区域,默认500bp
    #percent = 0.3

    if len(sys.argv) < 2:
        print ('please input parameters；or input --help to get the usage')
        sys.exit()
        # if sys.argv[1].startswith('--'):
        #   option = sys.argv[1][2:]
        # fetch sys.argv[1] but without the first two characters

    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        #     print callerDict
        inst = allCallerSimple(**callerDict)
        inst.run()