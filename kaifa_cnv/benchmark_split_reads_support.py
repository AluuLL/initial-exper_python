#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam
'''对benchmark区域开始以及结束10bp容忍范围内的split_reads支持度的统计'''



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


def count_split(inputItem):
    global inputFileBAMName
    global longth
    count=0
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    print inputItem
    for read in bamfile.fetch(inputItem[0], int(inputItem[1])-int(longth), int(inputItem[1])+int(longth)):
        if read.reference_end in range(int(inputItem[1])-int(longth),int(inputItem[1])+int(longth)+1):
            if read.cigartuples[-1][0] == pysam.CSOFT_CLIP  or  read.cigartuples[-1][0] == pysam.CHARD_CLIP:

                try:
                    SA_string = read.get_tag("SA")
                    print read
                    print SA_string
                    SA_list=SA_string.split(",")
                    if SA_list[0]==inputItem[0] and (int(SA_list[1]) in range(int(inputItem[2])-int(longth),int(inputItem[2])+int(longth)+1)):
                        count +=1


                except KeyError as E:
                    pass

    inputItem.append(str(count))
    print inputItem
    return inputItem


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
        # with concurrent.futures.ProcessPoolExecutor(max_workers=15) as executor :
        #     line = executor.map(count_mq,inputCBSInst)
        line = map(lambda x:count_split(x),inputCBSInst)
        # print (type(line))
        for item in line:
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
        -l(--long=)                                        :cbs tolerant paired reads region span ,faulut is 10bp
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
    long = 10         #cbs区域左右pair对容忍区域,默认10bp
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