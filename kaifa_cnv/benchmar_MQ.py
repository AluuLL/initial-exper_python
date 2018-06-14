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
    L_count = 0.000001
    R_count = 0.000001
    L_mq = 0.000001
    R_mq = 0.000001
    C_count = 0.000001
    C_mq = 0.000001
    # bamfile = pysam.AlignmentFile('/disk/lulu/tmp/hiseq_30x-1/hiseq_30x_1.sorted.bam', 'rb')
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')

    # for read in bamfile.fetch('1', 22975, 24200):
    #     print (read.reference_end)
    # tb = pysam.Tabixfile(inputFileBAMName)
    for read in bamfile.fetch(inputItem[0], int(inputItem[1]), int(inputItem[2])):
        # listcov = item.strip().split("\t")
        # if int(listcov[1]) >= (int(inputItem[2])-dis) and int(listcov[2]) <= int(inputItem[2]):
        #     L_count=L_count+1
        #     L_depth=L_depth+float(listcov[3])
        # if int(listcov[1]) >= int(inputItem[3]) and int(listcov[2]) <= (int(inputItem[3])+dis):
        #     R_count=R_count+1
        #     R_depth=R_depth+float(listcov[3])
        # if int(listcov[1])>=int(inputItem[2]) and int(listcov[2]) <= int(inputItem[3]):
        if read.reference_start >= int(inputItem[1]) and read.reference_end <= int(inputItem[2]):
            C_count = C_count + 1
            C_mq = C_mq + read.mapping_quality

    for read in bamfile.fetch(inputItem[0], int(inputItem[1]) - dis, int(inputItem[1])):
        # listcov = item.strip().split("\t")
        if read.reference_start >= (int(inputItem[1])-dis) and read.reference_end <= int(inputItem[1]):
            L_count = L_count + 1
            L_mq = L_mq + read.mapping_quality


    for read in bamfile.fetch(inputItem[0], int(inputItem[2]), int(inputItem[2]) + dis):
        # listcov = item.strip().split("\t")
        if read.reference_start >= int(inputItem[2]) and read.reference_end<= (int(inputItem[2])+dis):
            R_count = R_count + 1
            R_mq = R_mq + read.mapping_quality

    inputItem.append(str(round((C_mq / C_count), 2)))
    inputItem.append(str(round((L_mq / L_count), 2)))
    inputItem.append(str(round((R_mq / R_count), 2)))
    return inputItem


def a(x):
    print (x)
class allCallerSimple():
    def __init__(self, **kwargs):
        self.kwargs = kwargs



    def run(self):
        global inputFileBAMName
        inputFileCBSName = self.kwargs.get('inputFileCBSName')
        inputFileBAMName = self.kwargs.get('inputFileBAMName')
        distance = self.kwargs.get('distance')
        outputFileName = self.kwargs.get('outputFileName')
        ##
        try:
            F = open(outputFileName, 'w')
        except IOError:
            print ('IO error: %s' % (outputFileName))
            sys.exit(-1)

        inputCBSInst = FileIter(inputFileCBSName)
        # with concurrent.futures.ProcessPoolExecutor() as executor :
        #     for inputItem in inputCBSInst:
        with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor :
            line = executor.map(count_mq,inputCBSInst)
        # line = map(lambda x:count_mq(x),inputCBSInst)

        for item in  (list(line)):
            F.write('\t'.join(item) +'\n')
        F.close()



def param(argv):
    global inputfile_CBS
    global inputfile_BAM
    global outputfile
    global dis

    try:
        options, args = getopt.getopt(argv, "hi:b:o:d:",
                                      ["help", "inputCBS=", "inputBAM=","output=", "dis="])
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
        -d(--dis=)                                         :L_COV& R_COV span,fault is 500bp                                       
        ''')


def cmdDict():
    global inputfile_CBS
    global inputfile_BAM
    global outputfile
    global dis
    # global percent
    # global site
    # sitestr = site.strip().split(",")
    callerDict = {
        'inputFileCBSName': inputfile_CBS,
        'inputFileBAMName': inputfile_BAM,
        'outputFileName': outputfile,
        'distance': dis
    }

    return callerDict


if __name__ == '__main__':
    inputfile_CBS = "" #输入待求的CBS文件
    inputfile_BAM = "" #输入对应该CBS文件的cov文件
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