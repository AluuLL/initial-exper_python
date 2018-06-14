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

def CNV_length(inputItem):
    cnv_length=int(inputItem[3])-int(inputItem[2])
    inputItem.append(str(cnv_length))

    return inputItem

def SNP_chunhe(inputItem):
    global SNPFileName
    snpMAFvalue=[]  #该CBS区域内对应上得snp位点的MAF值
    snpNum=0   #所有snp点的个数
    MAFNum=0   #MAF值大于等于0.8的个数
    MAFratio=0 #MAFNum/snpNum

    tb = pysam.Tabixfile(SNPFileName)
    for item in tb.fetch(inputItem[1],int(inputItem[2]), int(inputItem[3])):
        snplist = item.strip().split("\t")
        if int(snplist[1]) in range(int(inputItem[2]),int(inputItem[3])+1):
            snpMAFvalue.append(snplist[16]) #在pup文件中第17列是MAF的值
            if float(snplist[16])>=0.8:
                MAFNum+=1
    snpNum=len(snpMAFvalue)
    if snpNum==0:
        MAFvaluemean=0
        snpNum=0
        inputItem.append(str(0)) #增加MAF-value-mean
        inputItem.append(str(0)) #增加All-SNP-num
        inputItem.append("None") #增加MAF-value-num(>=0.8)
        inputItem.append("None") #增加MAF-ratio(=MAF-value-num/All-SNP-num)
    else:
        MAFvalue=sum(map(lambda x:float(x),snpMAFvalue)) #MAF所有值得和
        MAFvaluemean=round(MAFvalue/snpNum, 2) #MAF均值
        MAFratio=round(MAFNum/snpNum,2) #MAF值大于等于0.8得占比
        inputItem.append(str(MAFvaluemean)) #增加MAF-value-mean
        inputItem.append(str(snpNum))       #增加All-SNP-num
        inputItem.append(str(MAFNum))       #增加MAF-value-num(>=0.8)
        inputItem.append(str(MAFratio))     #增加MAF-ratio(=MAF-value-num/All-SNP-num)
    # print inputItem
    return inputItem




    # with open(SNPFileName) as file:
    #     for line in file:
    #         snplist=line.strip().split("\t")
    #         if snplist[0]==inputItem[1] and snplist[1] in range(int(inputItem[2]),int(inputItem[3])+1):
    #             snpMAFvalue.append(snplist[16])
    #
    # print snpMAFvalue


def BaseQ(inputItem):
    global inputFileBAMName
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')
    # print inputItem[2]
    basequality=[]
    for pileupcolumn in bamfile.pileup(inputItem[1], int(inputItem[2]), int(inputItem[3])):
        if pileupcolumn.pos <int(inputItem[2])-1:
            continue
        else:
            # print pileupcolumn.pos,pileupcolumn.n
            for pileupread in pileupcolumn.pileups :
                if pileupread.indel==0 and pileupread.query_position!=None:
                    # print pileupread
                    # print pileupread.query_position
                    # print pileupread.alignment.query_alignment_length
                     basequality.append(pileupread.alignment.query_qualities[pileupread.query_position-1])
    base_quality_value=sum(basequality)
    base_quality_mean=round(base_quality_value/(len(basequality)),2)
    inputItem.append(str(base_quality_mean))#增加BaseQuality_mean
    print inputItem
    return inputItem








def count_mq(inputItem):
    global inputFileBAMName
    global distance   #CBS左右的范围,默认为500bp
    global longth     #CBS区域左右Pair对容忍区域，默认为500bp
    pair_reads_mapq = []
    pair_reads_cigarstring = []
    pair_reads_mismatch = []
    L_count = 0.000001
    R_count = 0.000001
    L_mq = 0.000001
    R_mq = 0.000001
    C_count = 0.000001
    C_mq = 0.000001
    reads_count=0
    pair_reads_count=0
    # bamfile = pysam.AlignmentFile('/disk/lulu/tmp/hiseq_30x-1/hiseq_30x_1.sorted.bam', 'rb')
    bamfile = pysam.AlignmentFile(inputFileBAMName, 'rb')

    for read in bamfile.fetch(inputItem[1], int(inputItem[2]), int(inputItem[3])):
        if read.reference_start >= int(inputItem[2]) and read.reference_end <= int(inputItem[3]):
            C_count = C_count + 1
            C_mq = C_mq + read.mapping_quality
    if int(inputItem[2])-int(distance) >=0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[2]) - int(distance), int(inputItem[2])):
            # listcov = item.strip().split("\t")
            if read.reference_start >= (int(inputItem[2])-int(distance)) and read.reference_end <= int(inputItem[2]):
                L_count = L_count + 1
                L_mq = L_mq + read.mapping_quality
    else:
        for read in bamfile.fetch(inputItem[1], 0, int(inputItem[2])):
            # listcov = item.strip().split("\t")
            if read.reference_start >= 0 and read.reference_end <= int(inputItem[2]):
                L_count = L_count + 1
                L_mq = L_mq + read.mapping_quality
    for read in bamfile.fetch(inputItem[1], int(inputItem[3]), int(inputItem[3]) + int(distance)):
        # listcov = item.strip().split("\t")
        if read.reference_start >= int(inputItem[3]) and read.reference_end<= (int(inputItem[3])+int(distance)):
            R_count = R_count + 1
            R_mq = R_mq + read.mapping_quality
    if (int(inputItem[2])-int(longth) >=0) and  (int(inputItem[3])-int(longth)) >=0:
        for read in bamfile.fetch(inputItem[1], int(inputItem[2]) - int(longth), int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <= 300 or read.reference_name != read.next_reference_name:
                continue
            else:
                reads_count=reads_count+1
                if read.next_reference_start >= (int(inputItem[3]) - int(longth)) and read.next_reference_start <= (int(inputItem[3]) + int(longth)):
                    pair_reads_count=pair_reads_count+1
                    pair_reads_mapq.append(read.mapq)
                    pair_reads_cigarstring.append(read.cigarstring == "150M")
                    # pair_reads_mismatch.append(get_n_mismatch(read))
    else:
        for read in bamfile.fetch(inputItem[1], 0, int(inputItem[2]) + int(longth)):
            if read.is_proper_pair or abs(read.template_length) <= 300 or read.reference_name != read.next_reference_name:
                continue
            else:
                reads_count=reads_count+1
                if (int(inputItem[3])-int(longth)) >=0:
                    if read.next_reference_start >= (int(inputItem[3]) - int(longth)) and read.next_reference_start <= (int(inputItem[3]) + int(longth)):
                        pair_reads_count=pair_reads_count+1
                        pair_reads_mapq.append(read.mapq)
                        pair_reads_cigarstring.append(read.cigarstring == "150M")
                        # pair_reads_mismatch.append(get_n_mismatch(read))
                else:
                    if read.next_reference_start >= 0 and read.next_reference_start <= (int(inputItem[3]) + int(longth)):
                        pair_reads_count=pair_reads_count+1
                        pair_reads_mapq.append(read.mapq)
                        pair_reads_cigarstring.append(read.cigarstring == "150M")
                        # pair_reads_mismatch.append(get_n_mismatch(read))

    if len(pair_reads_mapq)>0:
        pair_reads_mapq_mean = float(sum(pair_reads_mapq)) / len(pair_reads_mapq)
        pair_reads_150M_num = sum(pair_reads_cigarstring)

        if len(pair_reads_mismatch)>0:
            pair_reads_mismatch_mean = float(sum(pair_reads_mismatch)) / len(pair_reads_mismatch)
        else:
            pair_reads_mismatch_mean=0
    else:
        pair_reads_mapq_mean=0
        pair_reads_150M_num=0
        # pair_reads_mismatch_mean=0
    if reads_count==0:
        pair_reads_ratio=0
    else:
        pair_reads_ratio=float(pair_reads_count)/float(reads_count)
        # print pair_reads_ratio


    inputItem.append(str(round((L_mq / L_count), 2)))
    inputItem.append(str(round((C_mq / C_count), 2)))
    inputItem.append(str(round((R_mq / R_count), 2)))
    inputItem.append(str(len(pair_reads_mapq))) #pair_reads num
    inputItem.append(str(round(pair_reads_ratio, 2))) #pair_reads_ratio
    inputItem.append(str(round(pair_reads_mapq_mean,2)))
    inputItem.append(str(pair_reads_150M_num))
    # inputItem.append(str(round(pair_reads_mismatch_mean,2)))
    # print inputItem
    return inputItem

def count_cov(inputItem):
    global inputFileCOVName
    global distance
    L_count = 0.000001
    R_count = 0.000001
    L_depth = 0.000001
    R_depth = 0.000001
    C_count = 0.000001
    C_depth = 0.000001
    tb = pysam.Tabixfile(inputFileCOVName)
    for item in tb.fetch(inputItem[1], int(inputItem[2]), int(inputItem[3])):
        listcov = item.strip().split("\t")
        # if int(listcov[1])>=int(inputItem[2]) and int(listcov[2]) <= int(inputItem[3]):
        C_count = C_count + 1
        C_depth = C_depth + float(listcov[3])
    if int(inputItem[2]) -int(distance)>=0:
        for item in tb.fetch(inputItem[1], int(inputItem[2]) - int(distance), int(inputItem[2])):
            listcov = item.strip().split("\t")
            if int(listcov[2]) <= int(inputItem[2]):
                L_count = L_count + 1
                L_depth = L_depth + float(listcov[3])
    else:
        for item in tb.fetch(inputItem[1], 0, int(inputItem[2])):
            listcov = item.strip().split("\t")
            if int(listcov[2]) <= int(inputItem[2]):
                L_count = L_count + 1
                L_depth = L_depth + float(listcov[3])

    for item in tb.fetch(inputItem[1], int(inputItem[3]), int(inputItem[3]) + int(distance)):
        listcov = item.strip().split("\t")
        if int(listcov[1]) >= int(inputItem[3]):
            R_count = R_count + 1
            R_depth = R_depth + float(listcov[3])

    inputItem.append(str(round((L_depth / L_count), 2)))
    inputItem.append(str(round((C_depth / C_count), 2)))
    inputItem.append(str(round((R_depth / R_count), 2)))
    inputItem.append(str(round((C_depth/C_count)/(L_depth / L_count),2)))
    inputItem.append(str(round((C_depth/C_count)/(R_depth / R_count),2)))
    # print inputItem
    return inputItem


def a(x):
    print (x)


class feature_extraction():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        global inputFileBAMName
        global inputFileCOVName
        global distance
        global longth
        global SNPFileName
        inputFileCBSName = self.kwargs.get('inputFileCBSName')
        inputFileCOVName = self.kwargs.get('inputFileCOVName')
        inputFileBAMName = self.kwargs.get('inputFileBAMName')
        distance = self.kwargs.get('distance')
        outputFileName = self.kwargs.get('outputFileName')
        SNPFileName = self.kwargs.get('SNPFileName')
        longth = self.kwargs.get('longth')
        ##
        try:
            F = open(outputFileName, 'w')
        except IOError:
            print ('IO error: %s' % (outputFileName))
            sys.exit(-1)

        inputCBSInst = FileIter(inputFileCBSName)
        # with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor :
        #     line = executor.map(count_cov,inputCBSInst)
        # for i in inputCBSInst:
        #     print i
        #inputCBSinst是一个列表
        # line = map(lambda x:count_cov(x),inputCBSInst)   #L_COV\CNV_COV\R_COV\L_depth_ratio\R_depth_ratio
        # line = map(lambda x: CNV_length(x), inputCBSInst)#CNV_length
        # line = map(lambda x: SNP_chunhe(x), inputCBSInst)#MAF_value_mean\All-SNP-num\MAF_value_num(>=0.8)\MAF_ratio
        # line = map(lambda x: count_mq(x), inputCBSInst)  #L_mq\CNV_mq\R_mq\pair_reads_num\pair_reads_ratio\pair_reads_mapq_mean\pair_reads_150m_num
        line = map(lambda x: BaseQ(x), inputCBSInst)
        for item in  (list(line)):
            print item
            F.write('\t'.join(item) +'\n')
        F.close()



def param(argv):
    global inputfile_CBS
    global inputfile_COV
    global inputfile_BAM
    global SNPFile
    global outputfile
    global dis
    global long

    try:
        options, args = getopt.getopt(argv, "hi:v:o:d:s:l:b:",
                                      ["help", "inputCBS=", "inputCOV=","output=", "dis=","SNPFile=","long=", "inputBAM="])
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
        if option in ("-b", "--inputBAM"):
            inputfile_BAM = value
        if option in ("-s", "--SNPFile"):
            SNPFile = value
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
        -v(--inputCOV=) input .cov.gz file                 :input_file's chr &star&end column from 0 
        -b(--inputBAM=) input .bam file                    :input_bam_file
        -o(--output=)   outputfile                         :output_file
        -s(--SNPFile=)  SNP file
        -d(--dis=)                                         :L_COV& R_COV span,fault is 500bp 
        -l(--long=)                                        :cbs tolerant paired reads region span ,faulut is 500bp
        ''')


def cmdDict():
    global inputfile_CBS
    global inputfile_COV
    global inputfile_BAM
    global outputfile
    global dis
    global SNPFile
    global long
    # sitestr = site.strip().split(",")
    callerDict = {
        'inputFileCBSName': inputfile_CBS,
        'inputFileCOVName': inputfile_COV,
        'inputFileBAMName': inputfile_BAM,
        'SNPFileName': SNPFile,
        # 'inputStart': sitestr[1],
        # 'inputEnd': sitestr[2],
        'outputFileName': outputfile,
        'distance': dis,
        'longth': long

    }

    return callerDict


if __name__ == '__main__':
    inputfile_CBS = "" #输入待求的CBS文件
    inputfile_COV = "" #输入对应该CBS文件的cov文件，要事先使用tabix建索引并压缩，用作求左右depth以及ratio
    inputfile_BAM = "" #输入对应该CBS文件的bam文件,用作求pair_reads等相关信息
    outputfile = ""    #输出文件名
    SNP_file = ""      #SNP文件
    dis = 500          #左右surrounding范围的大小,默认500bp
    long = 500         #CBS区域左右pair对容忍区域,默认500bp
    if len(sys.argv) < 2:
        print ('please input parameters；or input --help to get the usage')
        sys.exit()

    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        inst = feature_extraction(**callerDict)
        inst.run()