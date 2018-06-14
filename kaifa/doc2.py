# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time
import json
from docxtpl import DocxTemplate


class FileIter():
    def __init__(self, fileName):
        try:
            self.file = open(fileName, 'r')
        except IOError as E:
            self.ERROR = True
            print "Can't open %s!" % (fileName)
            print E

    def next(self):
        line = self.file.readline()
        if line == '':
            raise StopIteration
        else:
            return line.strip('\n').split('\t')

    def __iter__(self):
        return self

class CCode:
    def str(self,content,encoding = 'utf-8'):
        return json.dumps(content,encoidng=encoding,ensure_ascii=False,indent=4)
        pass
    pass


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
        Prefixvalue = self.kwargs.get('PrefixName')
        DrawPath = self.kwargs.get('Draw_PathFile')
        outputFileName = Prefixvalue+".docx"
        ##
        # try:
        #     F = open(outputFileName, 'w')
        # except IOError:
        #     print 'IO error: %s' % (outputFileName)
        #     sys.exit(-1)
        SNVInst = FileIter(SNVFileName)
        IndelInst = FileIter(IndelFileName)
        CNVInst = FileIter(CNVFileName)
        # context = {'company_name': "World company"}  # company_name 是存在于1.docx文档里面的变量，就像这样{{company_name}}，直接放在1.docx文件的明确位置就行
        # doc.render(context)  # 这里是有jinjia2的模板语言进行变量的替换，然后便可以在1.docx文档里面看到{{company_name}}变成了World company
        self.autotable(SNVInst,'tbl_contents','SNV')
        self.autotable(IndelInst,'indel_contents','Indel')
        self.autotable(CNVInst,'cnv_contents','CNV')
        # for SNVItem in SNVInst:
        # context = {
        #     #'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
        #     'tbl_contents': [
        #         {'label': 'SNV', 'cols': [SNVItem[0], SNVItem[1], SNVItem[2], SNVItem[3], u'SNVItem[4]', SNVItem[5]]},
        #     ],
        #     # 'indel_contents': [
        #     #     {'label': 'yellow', 'cols': ['MAP6D1', '1', 'c.45C>T', 'p.R15R', u'同义突变', '67.86%']},
        #     #     {'label': 'red', 'cols': ['ZNF628', '3', 'c.700A>G', 'p.T234A', u'非同义突变', '61.46%']},
        #     #     {'label': 'green', 'cols': ['C2orf72', '1', 'c.36T>C', 'p.L12L', u'同义突变', '55.10%']},
        #     #     {'label': 'green', 'cols': ['ZIC5', '1', 'c.1254G>A', 'p.P418P', u'同义突变', '45.00%']},
        #     #
        #     # ],
        #     # 'cnv_contents': [
        #     #     {'value': ['ANKRD18A', u'拷贝数增加', '3']},
        #     #     {'value': ['CCDC73', u'拷贝数增加', '3']},
        #     #     {'value': ['CTSS', u'拷贝数增加', '3']},
        #     #     {'value': ['DUSP9', u'拷贝数增加', '3']},
        #     #     {'value': ['DUX4', u'拷贝数减少', '1']},
        #     #     {'value': ['FAM58A', u'拷贝数增加', '3']},
        #     # ]
        # }

        # doc.render(context)
        doc.save("/disk/lulu/autoreport/generated_doc.docx")  # 保存

    def autotable(self, inputInst, input_contents, type):
        global context
        # doc = DocxTemplate(r"/disk/lulu/autoreport/template.docx")
        # cCode = CCode()
        if type == "CNV":
            for InputItem in inputInst:
                # InputItems=cCode.str(InputItem)
                context = {
                    # 'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
                    input_contents: [
                        {'label': type, 'value': [InputItem[0], u'InputItem[1]', InputItem[2]]},
                    ],
                }
                doc.render(context)
        elif type =="SNV":
            context = {input_contents: []}
            for key,InputItem in enumerate(inputInst):
                i = InputItem[4].decode('utf-8').encode('utf-8')
                print i
                context[input_contents].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], u'i', InputItem[5]]})
            print context
            doc.render(context)
        else:
            context1 = {input_contents: []}
            for key,InputItem in enumerate(inputInst):
                i = InputItem[4].decode('utf-8').encode('utf-8')
                print i
                context1[input_contents].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], u'i', InputItem[5]]})
            print context1
            doc.render(context1)
            # context = {
            #     #     # 'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
            #         input_contents: [
            #             {'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], u'InputItem[4]', InputItem[5]]},
            #             {'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], u'InputItem[4]', InputItem[5]]},
            #         ]
            #     }
            # print context
                # doc.render(context)
            # for key,InputItem in enumerate(inputInst):
            #     input_contents = {'cols':[InputItem[0], InputItem[1], InputItem[2], InputItem[3], u'InputItem[4]', InputItem[5]],}
            # doc.render(input_contents)
            # print input_contents
                # context = {
                #     #'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
                #     'tbl_contents': [
                #         {'label': 'SNV', 'cols': [SNVItem[0], SNVItem[1], SNVItem[2], SNVItem[3], u'SNVItem[4]', SNVItem[5]]},
                #     ],
                #     # 'indel_contents': [
                #     #     {'label': 'yellow', 'cols': ['MAP6D1', '1', 'c.45C>T', 'p.R15R', u'同义突变', '67.86%']},
                #     #     {'label': 'red', 'cols': ['ZNF628', '3', 'c.700A>G', 'p.T234A', u'非同义突变', '61.46%']},
                #     #     {'label': 'green', 'cols': ['C2orf72', '1', 'c.36T>C', 'p.L12L', u'同义突变', '55.10%']},
                #     #     {'label': 'green', 'cols': ['ZIC5', '1', 'c.1254G>A', 'p.P418P', u'同义突变', '45.00%']},
                #     #]

                 # }


        #当然，这个包的功能远远不止上面例子中的一些，可以包含图片
        # myimage = InlineImage(doc, 'test_files/python_logo.png', width=Mm(20))  # tpl便是上面例子中的doc对象也可以包含另一个docx文档，
        # sub = doc.new_subdoc()
        # sub.subdocx = Document('d:\\2.docx').
        # doc.render({'sub': sub})



def param(argv):
    global CNV_File
    global SNV_File
    global Indel_File
    global Prefix
    global Draw_Path
#    global percent
    try:
        options, args = getopt.getopt(argv, "hC:S:I:P:D:", ["help", "CNV_File=", "SNV_File=", "Indel_File=","Prefix=","Draw_Path="])
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
        if option in ("-P", "--Prefix"):
            Prefix = value
        if option in ("-D","--Draw_Path"):
            Draw_Path = value
            # print (options,args)
    if args:
        print "error arrgs:%s .please input --help to get the usage" % args
    #print options,args

def usage():
    print '''
      This program can be filled the Word report content automatically.
      Options include:
        -C(--CNV_File=) CNV_File
        -S(--SNV_File=) SNV_File
        -I(--Indel_File=) Indel_File
        -P(--Prefix) OUTPUT_FILE'S PREFIX
        -D(--Draw_Path) Image Path
        '''


def cmdDict():
    global CNV_File
    global SNV_File
    global Indel_File
    global Prefix
    global Draw_Path
#    inputstr = inputfile.strip().split(",")
    callerDict = {
      #  'inputFileName': inputstr[0],
      #  'inputChr': inputstr[1],
      #  'inputStart': inputstr[2],
      #  'inputEnd': inputstr[3],
        'CNV_FileName': CNV_File,
        'SNV_FileName': SNV_File,
        'Indel_FileName': Indel_File,
        'PrefixName': Prefix,
        'Draw_PathFile': Draw_Path
    }
    return callerDict


if __name__ == '__main__':
    CNV_File = ""   #cnv文件的输入路径
    SVN_File = ""   #snv文件的输入路径
    Indel_File = "" #Indel文件的输入路径
    Prefix = ""     #输出word文档的前缀名
    Draw_Path = ""  #图片的输入路径接口
    if len(sys.argv) < 2:
        print 'please input parameters! or You can input "--help" to get the usage'
        sys.exit()
    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        print callerDict
        # print callerDict
        #      print inputfile
        #      print outputfile
        #      print db
        #      print percent
        inst = allCallerSimple(**callerDict)
        inst.run()

