# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import json
from docxtpl import DocxTemplate
import csv
#到此版本为止是可以实现突变结果和MMR\POL\新抗原的了。下一个版本主要加入实现页眉页脚和基本信息


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

class allCallerSimple():
    global doc
    doc= DocxTemplate(r"/disk/lulu/autoreport/template.docx")
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        global context
        CNVFileName = self.kwargs.get('CNV_FileName')
        SNVFileName = self.kwargs.get('SNV_FileName')
        IndelFileName = self.kwargs.get('Indel_FileName')
        # Prefixvalue = self.kwargs.get('PrefixName')
        # DrawPath = self.kwargs.get('Draw_PathFile')
        BasicInfoName = self.kwargs.get('Basic_InfoName')
        # HLAFileName = self.kwargs.get('HLA_FileName')
        NeoFileName = self.kwargs.get('Neo_FileName')
        MMRFileName = self.kwargs.get('MMR_FileName')
        POLFileName = self.kwargs.get('POL_FileName')
        # GeneDataName = self.kwargs.get('Gene_DataName')
        # RoadPathName = self.kwargs.get('Road_PathName')
        # outputFileName = Prefixvalue+".docx"

        SNVInst = FileIter(SNVFileName)
        IndelInst = FileIter(IndelFileName)
        CNVInst = FileIter(CNVFileName)
        NeoInst = FileIter(NeoFileName)
        MMRInst = FileIter(MMRFileName)
        POLInst = FileIter(POLFileName)
        BasicInst = FileIter(BasicInfoName)
        # context = {'company_name': "World company"}  # company_name 是存在于1.docx文档里面的变量，就像这样{{company_name}}，直接放在1.docx文件的明确位置就行
        # doc.render(context)  # 这里是有jinjia2的模板语言进行变量的替换，然后便可以在1.docx文档里面看到{{company_name}}变成了World company
        context={}
        self.autotable(SNVInst,IndelInst,CNVInst,MMRInst,POLInst,NeoInst,'SNV','Idel','CNV')
        doc.save("/disk/lulu/autoreport/output/generated_doc.docx")  # 保存

    def autotable(self, inputInst0, inputInst1, inputInst2,inputInst3, inputInst4, inputInst5, type1, type2, type3):
            global context
         # if not context:
            context = {'tbl_contents': [],'indel_contents':[],'cnv_contents':[],'MMR_contents':[],'POL_contents':[],'Neo_contents':[]}

            for InputItem in inputInst0:

                context['tbl_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], InputItem[5]]})

            for InputItem in inputInst1:
                context['indel_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], InputItem[5]]})
            for InputItem in inputInst2:
                    # InputItems=cCode.str(InputItem)
                context['cnv_contents'].append({'value': [InputItem[0], InputItem[1], InputItem[2]]})
            for InputItem in inputInst3:
                context['MMR_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4]]})
            for InputItem in inputInst4:
                context['POL_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4]]})
            for InputItem in inputInst5:
                context['Neo_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], InputItem[5]]})
            print (context)
            doc.render(context)

        #当然，这个包的功能远远不止上面例子中的一些，可以包含图片
        # myimage = InlineImage(doc, 'test_files/python_logo.png', width=Mm(20))  # tpl便是上面例子中的doc对象也可以包含另一个docx文档，
        # sub = doc.new_subdoc()
        # sub.subdocx = Document('d:\\2.docx').
        # doc.render({'sub': sub})



def param(argv):
    global CNV_File
    global SNV_File
    global Indel_File
    # global Prefix
    # global Draw_Path
    global Basic_Info
    # global HLA_File
    global Neo_File
    global MMR_File
    global POL_File
    # global Gene_Data
    # global Road_Path
    try:
        options, args = getopt.getopt(argv, "hC:S:I:N:M:P:B:",
            ["help", "CNV_File=", "SNV_File=", "Indel_File=", "Neo_File=", "MMR_File=", "POL_File=", "Basic_Info="])
        # options, args = getopt.getopt(argv, "hC:S:I:P:M:B:H:N:G:R", ["help", "CNV_File=", "SNV_File=", "Indel_File=","Prefix=","Draw_Path=","Basic_Info=","HLA_File=","Neo_File=","Gene_Data=","Road_Path="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for option, value in options:
        if not option:
            usage()
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        if option in ("-C", "--CNV_File"):
            CNV_File = value
        if option in ("-S", "--SNV_File"):
            SNV_File = value
        if option in ("-I", "--Indel_File"):
            Indel_File = value
        if option in ("-B","--Basic_Info"):
            Basic_Info = value
        # if option in ("-H", "--HLA_File"):
        #     HLA_File = value
        if option in ("-N", "--Neo_File"):
            Neo_File = value
        if option in ("-M", "MMR_File"):
            MMR_File = value
        if option in ("-P","POL_File"):
            POL_File = value
        # if option in ("-G", "--Gene_Data"):
        #     Gene_Data = value
        # if option in ("-R", "--Road_Path"):
        #     Road_Path = value

            # print (options,args)
    if args:
        print ("error arrgs:%s .please input --help to get the usage" % args)
    #print options,args

def usage():
    print ('''
      This program can be filled the Word report content automatically.
      Options include:
        -C(--CNV_File=) CNV_File
        -S(--SNV_File=) SNV_File
        -I(--Indel_File=) Indel_File
        -B(--Basic_Info) Basic_Info File whic contains the information of patient
        -H(--HLA_File) HLA_File 
        -N(--Neo_File) Neo_File which is Tumor neoantigen file
        -M(--MMR_File) MMR FILE
        -P(--POL_File) POL FILE
        -G(--Gene_Data) 1400Gene's function database
        -R(--Road_Path) Road Path Profile 
        ''')


def cmdDict():
    global CNV_File
    global SNV_File
    global Indel_File
    global Prefix
    global Draw_Path
    global Basic_Info
    # global HLA_File
    global Neo_File
    global MMR_File
    global POL_File
    # global Gene_Data
    # global Road_Path
#    inputstr = inputfile.strip().split(",")
    callerDict = {
        'CNV_FileName': CNV_File,
        'SNV_FileName': SNV_File,
        'Indel_FileName': Indel_File,
        # 'PrefixName': Prefix,
        # 'Draw_PathFile': Draw_Path,
        'Basic_InfoName': Basic_Info,
        # 'HAL_FileName': HLA_File,
        'Neo_FileName': Neo_File,
        'MMR_FileName': MMR_File,
        'POL_FileName': POL_File,
        # 'Gene_DataName': Gene_Data,
        # 'Road_PathName': Road_Path,
    }
    return callerDict


if __name__ == '__main__':
    CNV_File = ""   #cnv文件的输入路径
    SVN_File = ""   #snv文件的输入路径
    Indel_File = "" #Indel文件的输入路径
    # Prefix = ""     #输出word文档的前缀名
    # Draw_Path = ""  #图片的输入路径接口
    Basic_Info = "" #患者基本信息以及MSI图路径的配置文件（csv配置文件）
    # HLA_File = "" #HLA分型结果
    Neo_File = "" #新抗原结果文件
    MMR_File = "" #MMR文件
    POL_File= "" #POL文件
    # Gene_Data = "" #基因功能库
    # Road_Path = "" #路径配置文件：包括通路富集图的路径等内容的配置文件
    if len(sys.argv) < 2:
        print ('please input parameters! or You can input "--help" to get the usage')
        sys.exit()
    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        print (callerDict)
        # print callerDict
        #      print inputfile
        #      print outputfile
        #      print db
        #      print percent
        inst = allCallerSimple(**callerDict)
        inst.run()

