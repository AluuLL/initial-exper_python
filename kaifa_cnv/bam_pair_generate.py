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

def count_mq():
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
        if read.is_proper_pair or abs(int(read.reference_start)-int(read.next_reference_start)) >200000 or read.reference_name != read.next_reference_name:
            continue
        else:
            try:
                MC_string=read.get_tag("MC")
                print read
                # print MC_string
                MC_string_MIvalue_list=re.findall(r"([\d]*)[MI]",MC_string)
                mate_pair_reads_len=sum(map(lambda x:int(x),MC_string_MIvalue_list))
                next_reference_end=read.next_reference_start+int(mate_pair_reads_len)
                bam_list.append(str(read.reference_name))
                bam_list.append(str(read.reference_start))
                bam_list.append(str(read.reference_end))
                bam_list.append(str(read.next_reference_start))
                bam_list.append(str(next_reference_end))


            except KeyError as E:
                pass
        if bam_list:
            F.write('\t'.join(bam_list) + '\n')
    F.close()





class allCallerSimple():
    def __init__(self, **kwargs):
        self.kwargs = kwargs



    def run(self):
        global inputFileBAMName
        global outputFileName
        inputFileBAMName = self.kwargs.get('inputFileBAMName')
        outputFileName = self.kwargs.get('outputFileName')
        ##
        count_mq()




def param(argv):
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
        inst = allCallerSimple(**callerDict)
        inst.run()