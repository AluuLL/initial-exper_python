#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam
'''对benchmark区域（左边多500bp,右边多500bp）pair_reads对支持度的统计
    支持情况判定：左边500bp的reads在右边500bp是否有对用的Pair_reads
    if read.is_proper_pair or abs(read.template_length) <=300 or read.reference_id!=read.next_reference_id'''



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

def count_mq(inputItem):
    global inputFileBAMName
    global distance
    global longth
    count=0
    # bamfile = pysam.AlignmentFile('/disk/lulu/tmp/hiseq_30x-1/hiseq_30x_1.sorted.bam', 'rb')
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    print inputItem[1],inputItem[13],inputItem[14]
    # 0->1
    # 1->13
    # 2->14
    if int(inputItem[13])-int(longth)>=0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[13])-int(longth), int(inputItem[13])+int(longth)):
            if read.is_proper_pair or abs(read.template_length) <= 300 or read.reference_id != read.next_reference_id:
                continue
            else:
                if read.next_reference_start in range(int(inputItem[14])-int(longth),int(inputItem[14])+int(longth)+1):
                   count +=1
    else:
        for read in bamfile.fetch(inputItem[1], 0, int(inputItem[13])+int(longth)):
            if read.is_proper_pair or abs(read.template_length) <= 300 or read.reference_id != read.next_reference_id:
                continue
            else:
                if int(inputItem[14])-int(longth)>=0:
                    if read.next_reference_start in range(int(inputItem[14])-int(longth),int(inputItem[14])+int(longth)+1):
                       count +=1
                else:
                    if read.next_reference_start in range(0,int(inputItem[14])+int(longth)+1):
                       count +=1


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
        line = map(lambda x:count_mq(x),inputCBSInst)
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