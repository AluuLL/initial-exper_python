#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam

def generate_base_split():
    global inputFileBAMName
    global outputfileName
    try:
        F = open(outputFileName, 'w')
    except IOError:
        print ('IO error: %s' % (outputFileName))
        sys.exit(-1)

    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    for read in bamfile.fetch():
        bam_list = []
        try:
            SA_string = read.get_tag("SA")
            if (read.cigartuples[0][0] == pysam.CSOFT_CLIP or read.cigartuples[0][0] == pysam.CHARD_CLIP) and read.cigartuples[-1][0] == pysam.CMATCH:
                ref_state='H'
            elif read.cigartuples[0][0] == pysam.CMATCH and (read.cigartuples[-1][0] == pysam.CSOFT_CLIP or read.cigartuples[-1][0] == pysam.CHARD_CLIP):
                ref_state='T'
            elif (read.cigartuples[0][0] == pysam.CSOFT_CLIP or read.cigartuples[0][0] == pysam.CHARD_CLIP) and (read.cigartuples[-1][0] == pysam.CSOFT_CLIP or read.cigartuples[-1][0] == pysam.CHARD_CLIP):
                if read.cigartuples[0][1]>=read.cigartuples[-1][1]:
                    ref_state='H'
                else:
                    ref_state='T'
            SA_list = SA_string.split(",")
            if SA_list[0]==read.reference_name:
                # print read
                # print SA_string
                split_begin=SA_list[1] #根据SA的值，获得split reads对的起始位置
                split_read_len_list=re.findall(r"([\d]*)[MI]",SA_list[3]) #split_reads对的长度列表，即M/I的值列表
                split_reads_len = sum(map(lambda x: int(x), split_read_len_list)) #split_reads_len即是split_reads对的长度
                split_end=int(split_begin)+int(split_reads_len) #split_reads的end位置
                split_cigarlist=re.findall(r"([\d]*)([MINDSH=XPB])",SA_list[3]) #获取split的cigar元组
                # print split_cigarlist
                # print split_cigarlist[0][0],split_cigarlist[0][1]
                # print split_cigarlist[-1][0],split_cigarlist[-1][1]
                if (split_cigarlist[0][1] == 'S' or split_cigarlist[0][1] == 'H') and \
                                split_cigarlist[-1][1] == 'M':
                    split_state = 'H'
                elif split_cigarlist[0][1] == 'M' and (
                                split_cigarlist[-1][1] == 'S' or split_cigarlist[-1][1] == 'H'):
                    split_state = 'T'
                elif (split_cigarlist[0][1] == 'S' or split_cigarlist[0][1] == 'H') and (
                                split_cigarlist[-1][1] == 'S' or split_cigarlist[-1][1] == 'H'):
                    if split_cigarlist[0][0] >= split_cigarlist[-1][0]:
                        split_state = 'H'
                    else:
                        split_state = 'T'
                bam_list.append(str(read.reference_name))
                bam_list.append(str(read.reference_start))
                bam_list.append(str(read.reference_end))
                bam_list.append(str(ref_state))
                bam_list.append(str(split_begin))
                bam_list.append(str(split_end))
                bam_list.append(str(split_state))


        except KeyError as E:
            pass
        if bam_list:
            print bam_list
            F.write('\t'.join(bam_list) + '\n')
    F.close()





class Bam_Generate():
    def __init__(self, **kwargs):
        self.kwargs = kwargs



    def run(self):
        global inputFileBAMName
        global outputFileName
        inputFileBAMName = self.kwargs.get('inputFileBAMName')
        outputFileName = self.kwargs.get('outputFileName')
        ##
        generate_base_split()




def param(argv):
    global inputfile_CBS
    global inputfile_BAM
    global outputfile


    try:
        options, args = getopt.getopt(argv, "hi:b:o:d:l:",
                                      ["help","inputBAM=","output="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for option, value in options:
        if not option:
            usage()
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        if option in ("-o", "--output"):
            outputfile = value
        if option in ("-b", "--inputBAM"):
            inputfile_BAM = value


            # print (options,args)
    if args:
        print ("error arrgs:%s .please input --help to get the usage" % args)


def usage():
    print ('''
      This program can complish CBS file's surrounding depth caculate function.
      Options include:
        -b(--inputBAM=) input .bam file                    :input_file's chr &star&end column from 0 
        -o(--output=) outputfile                           :output_file 
        ''')


def cmdDict():
    global inputfile_BAM
    global outputfile

    callerDict = {
        'inputFileBAMName': inputfile_BAM,
        'outputFileName': outputfile,
    }

    return callerDict


if __name__ == '__main__':
    inputfile_BAM = "" #输入对应该CBS文件的cov文件
    outputfile = ""    #输出文件名

    if len(sys.argv) < 2:
        print ('please input parameters；or input --help to get the usage')
        sys.exit()


    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        #     print callerDict
        inst = Bam_Generate(**callerDict)
        inst.run()