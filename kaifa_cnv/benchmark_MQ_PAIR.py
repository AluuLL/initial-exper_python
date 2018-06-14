#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam
#mapping_quality和paired reads support 支持的个数整合



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

def get_n_mismatch(x):
    s = x.get_aligned_pairs(with_seq=True)
    if x.get_tag('NM') == 0:
        return 0
    n_mis = 0
    for item in s:
        if item[2] is None:
            continue
        if item[2].islower():
            n_mis = n_mis + 1
    return n_mis


def count_mq(inputItem):
    global inputFileBAMName
    global distance
    global longth
    pair_reads_mapq = []
    pair_reads_cigarstring = []
    pair_reads_mismatch = []
    L_count = 0.000001
    R_count = 0.000001
    L_mq = 0.000001
    R_mq = 0.000001
    C_count = 0.000001
    C_mq = 0.000001
    # bamfile = pysam.AlignmentFile('/disk/lulu/tmp/hiseq_30x-1/hiseq_30x_1.sorted.bam', 'rb')
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')

    for read in bamfile.fetch(inputItem[0], int(inputItem[1]), int(inputItem[2])):
        if read.reference_start >= int(inputItem[1]) and read.reference_end <= int(inputItem[2]):
            C_count = C_count + 1
            C_mq = C_mq + read.mapping_quality

    for read in bamfile.fetch(inputItem[0], int(inputItem[1]) - distance, int(inputItem[1])):
        # listcov = item.strip().split("\t")
        if read.reference_start >= (int(inputItem[1])-distance) and read.reference_end <= int(inputItem[1]):
            L_count = L_count + 1
            L_mq = L_mq + read.mapping_quality


    for read in bamfile.fetch(inputItem[0], int(inputItem[2]), int(inputItem[2]) + distance):
        # listcov = item.strip().split("\t")
        if read.reference_start >= int(inputItem[2]) and read.reference_end<= (int(inputItem[2])+distance):
            R_count = R_count + 1
            R_mq = R_mq + read.mapping_quality
    for read in bamfile.fetch(inputItem[0], int(inputItem[1]) - longth, int(inputItem[1]) + longth):
        if read.next_reference_start >= (int(inputItem[2]) - longth) and read.next_reference_start <= (int(inputItem[2]) + longth):
            pair_reads_mapq.append(read.mapq)
            pair_reads_cigarstring.append(read.cigarstring == "150M")
            pair_reads_mismatch.append(get_n_mismatch(read))
    if len(pair_reads_mapq)>0:
        pair_reads_mapq_mean = float(sum(pair_reads_mapq)) / len(pair_reads_mapq)
        pair_reads_150M_num = sum(pair_reads_cigarstring)
        pair_reads_mismatch_mean = float(sum(pair_reads_mismatch)) / len(pair_reads_mismatch)
    else:
        pair_reads_mapq_mean=0
        pair_reads_150M_num=0
        pair_reads_mismatch_mean=0

    inputItem.append(str(round((C_mq / C_count), 2)))
    inputItem.append(str(round((L_mq / L_count), 2)))
    inputItem.append(str(round((R_mq / R_count), 2)))
    inputItem.append(str(len(pair_reads_mapq))) #pair num
    inputItem.append(str(round(pair_reads_mapq_mean,2)))
    inputItem.append(str(pair_reads_150M_num))
    inputItem.append(str(round(pair_reads_mismatch_mean,2)))
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