#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam




class FileIter():
    context = {}
    def __init__(self, fileName):
        try:
            self.file = open(fileName, 'r')

        except IOError as E:
            self.ERROR = True
            print ("Can't open %s!" % (fileName))
            print (E)


    def __next__(self):
        line = self.file.readline()
        if line == '':
            raise StopIteration
        else:
            return line.strip('\n').split('\t')


    def __iter__(self):
        return self

def count_cov(inputItem):
    global inputFileCOVName
    L_count = 0.000001
    R_count = 0.000001
    L_depth = 0.000001
    R_depth = 0.000001
    C_count = 0.000001
    C_N_depth = 0.000001
    C_T_depth = 0.000001
    # tb = pysam.Tabixfile(inputFileCOVName)
    with open(inputFileCOVName) as tb:
        for item in tb:
            listcov = item.strip().split("\t")
            # if int(listcov[1]) >= (int(inputItem[2])-dis) and int(listcov[2]) <= int(inputItem[2]):
            #     L_count=L_count+1
            #     L_depth=L_depth+float(listcov[3])
            # if int(listcov[1]) >= int(inputItem[3]) and int(listcov[2]) <= (int(inputItem[3])+dis):
            #     R_count=R_count+1
            #     R_depth=R_depth+float(listcov[3])
            # if int(listcov[1])>=int(inputItem[2]) and int(listcov[2]) <= int(inputItem[3]):
            if listcov[0]==inputItem[1] and int(listcov[2]) <= int(inputItem[3]) and int(listcov[1])>=int(inputItem[2]):
                C_count = C_count + 1
                C_N_depth = C_N_depth + float(listcov[3])
                C_T_depth = C_T_depth + float(listcov[4])

    inputItem.append(str(round((C_N_depth / C_count), 2)))
    inputItem.append(str(round((C_T_depth / C_count), 2)))
    print (inputItem)
    return inputItem


def a(x):
    print (x)
class allCallerSimple():
    def __init__(self, **kwargs):
        self.kwargs = kwargs



    def run(self):
        global inputFileCOVName
        inputFileCBSName = self.kwargs.get('inputFileCBSName')
        inputFileCOVName = self.kwargs.get('inputFileCOVName')
        distance = self.kwargs.get('distance')
        outputFileName = self.kwargs.get('outputFileName')
        ##
        try:
            F = open(outputFileName, 'w')
        except IOError:
            print ('IO error: %s' % (outputFileName))
            sys.exit(-1)

        inputCBSInst = FileIter(inputFileCBSName)
        #with concurrent.futures.ProcessPoolExecutor() as executor :
            #for inputItem in inputCBSInst:
        # with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor :
        #     line = executor.map(count_cov,inputCBSInst)
        line = map(lambda x:count_cov(x),inputCBSInst)

        for item in  (list(line)):
            F.write('\t'.join(item) +'\n')
        F.close()



def param(argv):
    global inputfile_CBS
    global inputfile_COV
    global outputfile
    global dis

    try:
        options, args = getopt.getopt(argv, "hi:v:o:d:",
                                      ["help", "inputCBS=", "inputCOV=","output=", "dis="])
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
        if option in ("-v", "--inputCOV"):
            inputfile_COV = value

            # print (options,args)
    if args:
        print ("error arrgs:%s .please input --help to get the usage" % args)


def usage():
    print ('''
      This program can complish CBS file's surrounding depth caculate function.
      Options include:
        -i(--inputCBS=) input .gene file                    :inputCBSfile 
        -v(--inputCOV=) input .cov.gz file                 :input_file's chr &star&end column from 0 
        -o(--output=) outputfile                           :output_file                                       
        ''')


def cmdDict():
    global inputfile_CBS
    global inputfile_COV
    global outputfile
    global dis
    # global percent
    # global site
    # sitestr = site.strip().split(",")
    callerDict = {
        'inputFileCBSName': inputfile_CBS,
        'inputFileCOVName': inputfile_COV,
        # 'inputStart': sitestr[1],
        # 'inputEnd': sitestr[2],
        'outputFileName': outputfile,
        'distance': dis
        # 'dataBase': db,
        # 'Percent': percent
    }

    return callerDict


if __name__ == '__main__':
    inputfile_CBS = "" #输入待求的CBS文件
    inputfile_COV = "" #输入对应该CBS文件的cov文件
    outputfile = ""    #输出文件名
    dis =500           #前后surrounding的大小,默认500bp
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