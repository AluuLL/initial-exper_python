# !/usr/bin/python
# -*- coding: utf-8 -*-
#自动化生成报告V1.1版本，结直肠癌报告生成逻辑
import sys
import getopt
import re
from itertools import *
import time
import json
import csv
import codecs
from docxtpl import InlineImage
from docx.shared import Mm, Inches, Pt
import re
from docxtpl import DocxTemplate, RichText

##此版本是整合了所有功能模块的完整合集并且该模块是第二次更改用药提示模块：卢露露|2018年1月29日。

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

    def checkPoint(self,TMBFileName, NeoStatisFileName, MMRFileName, POLFileName):
        global mmr_mean
        global tmb_mean
        with open(TMBFileName, 'r', encoding='utf-8') as snv:
            line = snv.readlines()[1]
            line = line.strip('\n').split('\t')
            nonsys_num = int(line[1])
            sys_num = int(line[2])
            if line[3] == '-':
                kaks = 'N/A'
            else:
                kaks = round(float(line[3]), 2)
            tmb_result = round(float(line[6]), 2)
        with open(NeoStatisFileName, 'r', encoding='utf-8') as neo:
            line = neo.readline()
            line = line.strip('\n').split('\t')
            neo_num = int(line[1])
            # tnb_mean = line[2]
        with open(MMRFileName, 'r', encoding='utf-8') as mmr:
            mmr_Benign = 1
            for line in mmr:
                line = line.strip('\n').split('\t')
                if line[4] != "良性":
                    mmr_Benign = 0
                    break
        with open(POLFileName, 'r', encoding='utf-8') as pol:
            pol_Benign = 1
            for line in pol:
                line = line.strip('\n').split('\t')
                if line[4] != "良性":
                    pol_Benign = 0
                    break

        ######################TMB
        global tmb_mean
        if tmb_result >= 5.49:
            tmb_mean = '高'
        elif tmb_result < 2.86:
            tmb_mean = '低'
        else:
            tmb_mean = '中'
        #
        if nonsys_num >= 192:
            nonsys_mean = '高'
            tmb_des = "相较于ICGC-TCGA国际肿瘤基因组数据库的肺癌样本数据，本检测得到的TMB结果高于平均值，属于CheckMate 026中定义的全外显子组TMB-H（大于等于243个非同义突变位点）；"
        elif nonsys_num < 100:
            nonsys_mean = '低'
            tmb_des = "相较于ICGC-TCGA国际肿瘤基因组数据库的肺癌样本数据，本检测得到的TMB结果低于平均值，属于CheckMate 026中定义的全外显子组TMB-L（小于100个非同义突变位点）；"
        else:
            nonsys_mean = '中'
            tmb_des = "相较于ICGC-TCGA国际肿瘤基因组数据库的肺癌样本数据，本检测得到的TMB结果位于中位数附近，属于CheckMate 026中定义的全外显子组TMB-M（100-243个非同义突变位点）；"
        #
        if sys_num >= 77:
            sys_mean = '高'
        elif sys_num < 40:
            sys_mean = '低'
        else:
            sys_mean = '中'
        #
        if kaks == 'N/A':
            kaks_mean = 'N/A'
            kaks_des = RichText('')
        elif kaks >= 3:
            kaks_mean = '较高'
            kaks_des = RichText('\n＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio大于3.0，反映样本中的肿瘤细胞的增殖能力处于较高状态；',style='HLAMeanStyle')
        elif kaks < 2.5:
            kaks_mean = '较低'
            kaks_des = RichText('\n＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，通常肿瘤的A/S ratio大于2.5，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio小于2.5，反映样本中的肿瘤细胞的增殖能力处于较低状态；',style='HLAMeanStyle')
        else:
            kaks_mean = '中性'
            kaks_des = RichText('\n＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，通常肿瘤的A/S ratio大于2.5，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio略大于2.5，反映样本中的肿瘤细胞的增殖能力处于中性状态；',style='HLAMeanStyle')
        #
        if mmr_Benign == 1:
            mmr_result = "未发现致病/可能致病突变"
            mmr_mean = "正常"
        else:
            mmr_result = "发现致病/可能致病突变"
            mmr_mean = "异常"
        #
        if pol_Benign == 1:
            pol_result = "未发现致病/可能致病突变"
            pol_mean = "正常"
        else:
            pol_result = "发现致病/可能致病突变"
            pol_mean = "异常"
        content = {
            'tmb_result': str(tmb_result) + '/Mb',
            'tmb_mean': tmb_mean,
            'nonsys_num': str(nonsys_num) + '个',
            'nonsys_mean': nonsys_mean,
            'sys_num': str(sys_num) + '个',
            'sys_mean': sys_mean,
            'kaks_value': kaks,
            'kaks_des':kaks_des,
            'kaks_mean': kaks_mean,
            'mmr_result': mmr_result,
            'mmr_mean': mmr_mean,
            'pol_result': pol_result,
            'pol_mean': pol_mean,
            'neo_num': str(neo_num) + '个',
            'tmb_des': tmb_des,

        }
        return content

    def separateHLA(self,HLA):
        HLA_A = []
        HLA_B = []
        HLA_C = []
        for item in HLA:
            item = item[4:]  ###delete HLA-
            if re.match('^A', item) is not None:
                HLA_A.append(item)
            if re.match('^B', item) is not None:
                HLA_B.append(item)
            if re.match('^C', item) is not None:
                HLA_C.append(item)
        content = {
            'cols': ['\n'.join(HLA_A), '\n'.join(HLA_B), '\n'.join(HLA_C)],
            'value': {'A': HLA_A, 'B': HLA_B, 'C': HLA_C}
        }
        return content

    def getHeterozy(self,HLA):
        if len(HLA) == 1:
            return 'isozy'  ##纯合
        elif len(HLA) == 0:
            return 'NA'  # 无
        else:
            return 'heterozy'  # 杂合

    def getMean(self,normal, tumor):
        mean = RichText('注：人群的HLA-I分型存在广泛的多态性，本报告所列举的HLA-I分型结果由基因测序获得',style = "HLAMeanStyle")
        B62 = ['B*15:02', 'B*15:12', 'B*15:13', 'B*46:01', 'B*52:01']
        B44 = ['B*18:01', 'B*37:01', 'B*40:01', 'B*40:02', 'B*40:06', 'B*44:02', 'B*44:03', 'B*45:01']
        PD1 = ['B*15:01'] + B62 + B44
        ####
        if self.getHeterozy(normal['A']) == 'heterozy' and self.getHeterozy(normal['B']) == 'heterozy' and self.getHeterozy(
                normal['C']) == 'heterozy':
            mean.add(
                '\n＊本次检测从正常体细胞检测到所有的等位基因都处于杂合状态，最新研究显示相较于至少一个位置的等位基因为纯合状态的患者，全部为杂合状态的患者在接受anti-PD-1药物治疗时生存期中位数更长（Chowell ',style="HLAMeanStyle")
            mean.add('et al., Science）', italic=True,style = "HLAMeanStyle")
            if self.getHeterozy(tumor['A']) == 'heterozy' and self.getHeterozy(tumor['B']) == 'heterozy' and self.getHeterozy(
                    tumor['C']) == 'heterozy':
                mean.add('\n＊40%的非小细胞肺癌患者的肿瘤样本中检测到HLA-I的杂合性缺失，这与亚克隆的新抗原负载高相关（McGranahan ',style = "HLAMeanStyle")
                mean.add('et al., Cell', italic=True,style = "HLAMeanStyle")
                mean.add('），而本次检测未发现肿瘤样本和正常体细胞中存在HLA-I的分型差异',style = "HLAMeanStyle")
        if self.getHeterozy(normal['A']) == 'isozy' or self.getHeterozy(normal['B']) == 'isozy' or self.getHeterozy(
                normal['C']) == 'isozy':
            mean.add(
                '\n＊本次检测从正常细胞中检测到存在至少一个等位基因为纯合状态，根据最新研究显示相较于所有等位基因都处于杂合状态的患者，至少一个等位基因为纯合状态的患者在接受anti-PD-1药物治疗时生存期中位数较短（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add(')',style="HLAMeanStyle")
        ###
        if len(set(normal['B']) & set(B62)) > 0 and len(set(tumor['B']) & set(B62)) > 0:
            mean.add('\n＊最新研究显示携带有HLA-B62 supertype的等位基因的患者接受anti-PD-1治疗的预后较差（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从正常细胞和肿瘤组织中都检测到HLA-B62 supertype中的等位基因',style = "HLAMeanStyle")
        elif len(set(normal['B']) & set(B62)) == 0 and len(set(tumor['B']) & set(B62)) > 0:
            mean.add('\n＊最新研究显示携带有HLA-B62 supertype的等位基因的患者接受anti-PD-1治疗的预后较差（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从肿瘤组织中检测到HLA-B62 supertype中的等位基因',style = "HLAMeanStyle")
        elif len(set(normal['B']) & set(B62)) > 0 and len(set(tumor['B']) & set(B62)) == 0:
            mean.add('\n＊最新研究显示携带有HLA-B62 supertype的等位基因的患者接受anti-PD-1治疗的预后较差（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从正常细胞中检测到HLA-B62 supertype中的等位基因',style = "HLAMeanStyle")
        ###
        if 'B*15:01' in normal['B'] and 'B*15:01' in tumor['B']:
            mean.add(
                '\n＊最新研究显示携带有HLA-B62 supertype的B*15:01等位基因的患者接受anti-PD-1治疗的预后较差，这可能是因为B*15:01 的分子结构会影响T细胞对肿瘤细胞的识别能力（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从正常组织和肿瘤组织中都检测到B*15:01',style = "HLAMeanStyle")
        elif not 'B*15:01' in normal['B'] and 'B*15:01' in tumor['B']:
            mean.add(
                '\n＊最新研究显示携带有HLA-B62 supertype的B*15:01等位基因的患者接受anti-PD-1治疗的预后较差，这可能是因为B*15:01 的分子结构会影响T细胞对肿瘤细胞的识别能力（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从肿瘤组织中检测到B*15:01',style = "HLAMeanStyle")
        elif 'B*15:01' in normal['B'] and not 'B*15:01' in tumor['B']:
            mean.add(
                '\n＊最新研究显示携带有HLA-B62 supertype的B*15:01等位基因的患者接受anti-PD-1治疗的预后较差，这可能是因为B*15:01 的分子结构会影响T细胞对肿瘤细胞的识别能力（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从正常细胞中检测到B*15:01',style = "HLAMeanStyle")
        ###
        if len(set(normal['B']) & set(B44)) > 0 and len(set(tumor['B']) & set(B44)) > 0:
            mean.add('\n＊最新研究显示携带有HLA-B44 supertype的等位基因的患者接受anti-PD-1治疗的生存期中位数更长（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从正常细胞和肿瘤组织中都检测到HLA-B44 supertype中的等位基因',style = "HLAMeanStyle")
        elif len(set(normal['B']) & set(B44)) == 0 and len(set(tumor['B']) & set(B44)) > 0:
            mean.add('\n＊最新研究显示携带有HLA-B44 supertype的等位基因的患者接受anti-PD-1治疗的生存期中位数更长（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从肿瘤组织中检测到HLA-B44 supertype中的等位基因',style = "HLAMeanStyle")
        elif len(set(normal['B']) & set(B44)) > 0 and len(set(tumor['B']) & set(B44)) > 0:
            mean.add('\n＊最新研究显示携带有HLA-B44 supertype的等位基因的患者接受anti-PD-1治疗的生存期中位数更长（Chowell ',style = "HLAMeanStyle")
            mean.add('et al., Science', italic=True,style = "HLAMeanStyle")
            mean.add('），本次检测从正常细胞中检测到HLA-B44 supertype中的等位基因',style = "HLAMeanStyle")
        #####
        if len(set(normal['B']) & set(PD1)) == 0 and len(set(tumor['B']) & set(PD1)) == 0:
            mean.add('\n＊本次检测未发现任何已知的影响anti-PD-1治疗预后的HLA等位基因',style = "HLAMeanStyle")
        ###
        # mean='\n'.join(mean)
        return mean

    def HLA(self,HLAFileName):
        with open(HLAFileName, 'r', encoding='utf-8') as hla:
            line = hla.readlines()
            # print (line[1])
            normal = line[0].strip('\n').split(',')
            tumor = line[1].strip('\n').split(',')
            normal = self.separateHLA(normal)
            tumor = self.separateHLA(tumor)

            mean = self.getMean(normal['value'], tumor['value'])
        content = {
            'hla_contents': [
                {'label': '正常细胞中的HLA-I分型：', 'cols': normal['cols']},
                {'label': '肿瘤组织中的HLA-I分型：', 'cols': tumor['cols']}
            ],
            'hla_mean': mean
        }
        return content

    def fill_basicinfo(self,BasicInfo):
        global date_today
        date_today = time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        csvFile = codecs.open(BasicInfo, "r", 'gbk')
        reader = csv.DictReader(csvFile)
        name = []
        sample_id = []
        sex = []
        age = []
        tel =[]
        send_hospital = []
        send_doctor = []
        send_sample = []
        send_date = []
        diagnose_agency = []
        diagnose = []
        stage = []
        medi_history = []
        test_item = []
        receive_date = []
        report_date = []
        DNAng = []
        MSI = []
        testplatform = []
        BAT_25 =[]
        BAT_26 =[]
        NR_21 =[]
        NR_24=[]
        MONO_27 = []
        position =0
        global context
        global given_id
        global SAMPLEID
        global realMSI
        global realtestplatform
        global realBAT_25
        global realBAT_26
        global realNR_21
        global realNR_24
        global realMONO_27
        given_id=  SAMPLEID
        n=0
        # 样品名，可以作为该函数的参数进行传入。传入之前可以根据随意一个输出文件的名字来得到。
        for row in reader:
            # print (row)
            name.append(row['姓名'])
            sample_id.append(row['样本编号'])
            sex.append(row['性别'])
            age.append(row['年龄'])
            tel.append(row['联系方式'])
            send_hospital.append(row['送检医院'])
            send_doctor.append(row['送检医师'])
            send_sample.append(row['送检样本'])
            send_date.append(row['送样日期'])
            diagnose_agency.append(row['临床诊断机构'])
            diagnose.append(row['病理诊断'])
            stage.append(row['分期'])
            medi_history.append(row['用药史'])
            test_item.append(row['检测项目'])
            receive_date.append(row['收样日期'])
            DNAng.append(row['DNA总量(ng)'])
            MSI.append(row['MSI'])
            testplatform.append(row['测序平台'])
            BAT_25.append(row['BAT-25'])
            BAT_26.append(row['BAT-26'])
            NR_21.append(row['NR-21'])
            NR_24.append(row['NR-24'])
            MONO_27.append(row['MONO-27'])
        if given_id in sample_id:
            position = sample_id.index(given_id)
        realName = name[position]
        realsex = sex[position]
        realage =age[position]
        realtel = tel[position]
        realsend_hospital = send_hospital[position]
        realsend_doctor = send_doctor[position]
        realsend_sample = send_sample[position]
        realsend_date =send_date[position]
        realdiagnose_agency = diagnose_agency[position]
        realdiagnose = diagnose[position]
        realstage = stage[position]
        realmedi_history = medi_history[position]
        realtest_item = test_item[position]
        realreceive_date = receive_date[position]
        realDNAng = DNAng[position]
        realMSI = MSI[position]
        realtestplatform = testplatform[position]
        realBAT_25=BAT_25[position]
        realBAT_26=BAT_26[position]
        realNR_21=NR_21[position]
        realNR_24=NR_24[position]
        realMONO_27=MONO_27[position]
        # print (realmedi_history)
        # print (realdiagnose)
        # print (realMSI)
        # print (realtestplatform)
        # print (realMONO_27)
        # print (realBAT_25)
        csvFile.close()
        if realBAT_25 =='检测到长度变异':
            n=n+1
        if realBAT_26 == '检测到长度变异':
            n=n+1
        if realNR_21=='检测到长度变异':
            n=n+1
        if realNR_24=='检测到长度变异':
            n=n+1
        if realMONO_27=='检测到长度变异':
            n=n+1
        if n == 0:
            msi_mean = '未检测到串联重复序列长度变异'
            msi_des = RichText(
                '\n＊微卫星不稳定系统地比较了肿瘤和正常组织中串联重复序列的长度变异情况，根据变异程度划分为微卫星不稳定性高、低和微卫星稳定，其中微卫星不稳定性高的患者具有较好的免疫治疗预后，MSI的本次检测结果为微卫星稳定，即MSI-S；',
                style='HLAMeanStyle')
        if n==1:
            msi_mean ='检测到1个串联重复序列长度变异'
            msi_des =RichText(
                '\n＊微卫星不稳定系统地比较了肿瘤和正常组织中串联重复序列的长度变异情况，根据变异程度划分为微卫星不稳定性高、低和微卫星稳定，其中微卫星不稳定性高的患者具有较好的免疫治疗预后，MSI的本次检测结果为微卫星不稳定性低，即MSI-L；',
                style='HLAMeanStyle')
        if n ==2:
            msi_mean = '检测到2个串联重复序列长度变异'
            msi_des =RichText(
                '\n＊微卫星不稳定系统地比较了肿瘤和正常组织中串联重复序列的长度变异情况，根据变异程度划分为微卫星不稳定性高、低和微卫星稳定，其中微卫星不稳定性高的患者具有较好的免疫治疗预后，MSI的本次检测结果为微卫星不稳定性高，即MSI-H；',
                style='HLAMeanStyle')
        if n ==3:
            msi_mean = '检测到3个串联重复序列长度变异'
            msi_des =RichText(
                '\n＊微卫星不稳定系统地比较了肿瘤和正常组织中串联重复序列的长度变异情况，根据变异程度划分为微卫星不稳定性高、低和微卫星稳定，其中微卫星不稳定性高的患者具有较好的免疫治疗预后，MSI的本次检测结果为微卫星不稳定性高，即MSI-H；',
                style='HLAMeanStyle')
        if n == 4:
            msi_mean = '检测到4个串联重复序列长度变异'
            msi_des =RichText(
                '\n＊微卫星不稳定系统地比较了肿瘤和正常组织中串联重复序列的长度变异情况，根据变异程度划分为微卫星不稳定性高、低和微卫星稳定，其中微卫星不稳定性高的患者具有较好的免疫治疗预后，MSI的本次检测结果为微卫星不稳定性高，即MSI-H；',
                style='HLAMeanStyle')
        if n==5:
            msi_mean = '检测到5个串联重复序列长度变异'
            msi_des =RichText(
                '\n＊微卫星不稳定系统地比较了肿瘤和正常组织中串联重复序列的长度变异情况，根据变异程度划分为微卫星不稳定性高、低和微卫星稳定，其中微卫星不稳定性高的患者具有较好的免疫治疗预后，MSI的本次检测结果为微卫星不稳定性高，即MSI-H；',
                style='HLAMeanStyle')

        # print (n)
        context = {'name': realName, 'sex': realsex, 'age': realage, 'tel': realtel, 'send_hospital': realsend_hospital,
                   'send_doctor': realsend_doctor, 'send_sample': realsend_sample,
                   'send_date': realsend_date, 'diagnose_agency': realdiagnose_agency,
                   'diagnose':realdiagnose, 'stage': realstage, 'medi_history': realmedi_history,
                   'test_item':realtest_item, 'receive_date': realreceive_date, 'sample_id': given_id,
                   'report_date': date_today, 'DNAng': realDNAng,'msi_value':realMSI,'msi_mean':msi_mean,'msi_des':msi_des}
        context['report_date1'] =RichText(date_today,underline=True)

    def fill_msiimage(self,MSIPath):
        global context
        realMSI_path = InlineImage(doc,MSIPath,height=Mm(67),width=Mm(146.4))
        context['msiimage'] = realMSI_path


    def fillqc(self,QCpath):
        global context
        QCInst = FileIter(QCpath)
        for QCItem in QCInst:
            context = {'read':QCItem[0], 'depth': QCItem[1], 'cover': QCItem[2]}

    def fillpathway(self,pathway):
        global context
        realpathway_path =InlineImage(doc,pathway,height=Mm(73.3),width=Mm(146.5))
        context['pathwayimage'] = realpathway_path

    def medication(self):
        global context
        # print (realMSI)
        # print (mmr_mean)
        # print (tmb_mean)
        if ((realMSI == 'MSI-H'and mmr_mean == "异常")or (realMSI =='MSI-H' and mmr_mean =='正常') or ((realMSI =='MSI-S'or realMSI =='MSI-L') and mmr_mean == '异常') )and tmb_mean == '高':
            Nivolumab_mean = RichText('• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（CheckMate-026a）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 最新临床试验后的探索性研究数据显示，TMB高的晚期非小细胞肺癌患者接受Nivolumab治疗比化疗可获得更长的无进展生存期（CheckMate-026b）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• CheckMate-227临床试验的初步结果表明，Nivolumab和ipilimumab联合用药可用于TMB高的非小细胞肺癌患者的一线治疗中（CheckMate-227）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和良好的响应率,且PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（CheckMate-012a）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应（CheckMate-012b）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用,在2年整体生存率上高达62%。（CheckMate-012c）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（CheckMate-063）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞肺癌患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（CheckMate-057，CheckMate-017）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 最新临床试验后的探索性研究数据显示，广泛期小细胞肺癌患者不论在接受Nivolumab联合Ipilimumab治疗，还是Nivolumab单药治疗中，TMB高的患者比TMB中和低的患者，在客观响应率和12个月生存率都有明显提升（CheckMate-032）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗可获得良好的治疗效果（NCT00730639）。',
                               style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（TPS>=50%），可以考虑在一线治疗中使用Pembrolizumab（KEYNOTE-024）；\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与Pemetrexed和Carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（KEYNOTE-021）；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrozulimab在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好(KEYNOTE-001a)；\n',
                                   style="HLAMeanStyle")
            # Pembrolizumab_mean.add('• 2017年，FDA批准Prembrolizumab可用于治疗MSI-H或dMMR的无法手术切除或晚期转移性实体瘤患者（前期治疗进站后没有可行的替代方案，FDA批准适应症）\n',
            #     style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于治疗在铂类药物化疗后进展且PD-L1表达（TPS>=1%）的非小细胞肺癌患者（KEYNOTE-010）；\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Prembrolizumab可用于前期治疗进展后没有可行的替代方案，且MSI-H或dMMR的无法手术切除或晚期转移性实体瘤患者（FDA批准适应症）；\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（KEYNOTE-028）；\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（KEYNOTE-001b）。',
                style="HLAMeanStyle")
            Atezolizumab_mean = RichText('• 临床试验表明Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率（BIRCH）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• FDA批准在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，建议使用Atezolizumab进行后续治疗，且PD-L1在肿瘤细胞和浸润淋巴细胞中的表达水平与治疗疗效呈正相关（POPLAR）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• FDA批准在接受过先期治疗的非小细胞肺癌患者，可以考虑使用Atezolizumab进行后续治疗（OAK）。',
                                  style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab可作为不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC）；\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1表达高（TPS>=25%）的晚期非小细胞肺癌患者在接受Durvalumab治疗时，比PD-L1表达低或不表达的患者，存在明显的响应率和生存期获益（Study 1108）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ATLANTIC）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 非小细胞肺癌患者中正在开展的3个关于Durvalumab药物的三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC，MYSTIC，NEPTUNE）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者，旨在评估PD-L1高表达和PD-L1低表达分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tATLANTIC Phase II：临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ORR: 16.4% vs. 7.5%）。\n•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期NSCLC患者中，表现出良好的耐受性和响应率（ORR：26%-31%）。\n•\tCheckMate-012a Phase I：临床试验纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和高的响应率，PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（ORR: 47 vs. 38%; ORR with PD-L1 TPS≥1%: 57% vs. 57%）。\n•\tCheckMate-012b Phase I：临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应(Aes: 71%; ORR 23%; 6-month PFS: 41%; Median OS 19.4; 12-month and 18-month OS: 73% and 57%)。\n•\tCheckMate-012c Phase I：临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用虽然在AE导致的治疗终止率上比单药高，但在2年整体生存率上却达到了62%（ORR: 43%，24-month OS: 62%）。\n•\tCheckMate-017 Phase III：转移性鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n•\tCheckMate-026a Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。\n•\tCheckMate-026b Phase III：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n•\tCheckMate-032 Phase I/II：Nivolumab单药治疗，以及Nivolumab与Ipilimumab联合治疗在接受过治疗的广泛期小细胞肺癌患者中表现出持久的抗肿瘤活性和可控的安全性，TMB高的SCLC患者比TMB低的患者，客观响应率和1年期生存率都有明显提升（ORR: 46% vs. 16%; 1-year OS: 62% vs. 20%）。\n•\tCheckMate-057 Phase III：转移性非鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n•\tCheckMate-063 Phase II：临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（ORR: 14.5%; Adverse events: 17%）。\n•\tCheckMate-227 Phase III ：CheckMate-227临床试验的初步结果表明在晚期非小细胞肺癌患者的一线治疗中，如果患者TMB高，则使用Nivolumab和ipilimumab联合用药比化疗可获得更长的无进展生存期（Median PFS: 9.7 vs. 5.8）。\n•\tFDA批准适应症：根据KEYNOTE-016， KEYNOTE-164， KEYNOTE-012， KEYNOTE-028，KEYNOTE-158回溯性或/和前瞻性的临床试验结果，FDA批准Pembrolizumab用于治疗微卫星高度不稳定（MSI-H）/DNA错配修复基因缺失（dMMR）的实体瘤患者。\n•\tImpower 150 Phase III：临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时（64% VS 48%），明显降低了疾病进展和死亡的风险（PFS 8.3 vs. 6.4）。\n•\tKEYNOTE-001a Phase Ib：临床试验表明帕姆单抗在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好（PD-L1 TPS>=50% vs. ALL，ORR： 51% vs. 27%；12-month PFS： 54% vs. 35%；12-month OS： 85% vs. 71%）。\n•\tKEYNOTE-001b Phase Ib：临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（Median PFS: 4.4 vs. 2.1，Median PFS: 6.3 （颅外放射） vs. 2.0，Median OS: 10.7 vs. 5.3，Median OS: 11.6 vs. 5.3）。\n•\tKEYNOTE-010 Phase II/ III：在使用铂药化疗后进展且PD-L1表达（TPS >1%）的NSCLC患者中，接受Pembrolizumab治疗（10mg/kg每三周一次）比接受Docetaxel治疗，在生存期中位数上有110%的延长。\n•\tKEYNOTE-021 Phase II： 在非鳞性晚期NSCLC的一线治疗中Pembrolizumab、Pemetrexed和Carboplatin的联合用药是有效且可耐受的。三种药物的联合使用比仅使用化疗药物具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n•\tKEYNOTE-024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n•\tKEYNOTE-028 Phase Ib：临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（ORR: 33%）。\n•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tNCT00730639 Phase I：临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗在可控的安全范围内获得良好的中位整体生存期和整体生存率（Median OS: 9.9; 12-month OS: 42%; Adverse events: 14%）。\n•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tOAK Phase III：临床试验证明在先期治疗后的非小细胞肺癌患者中，使用Atezolizumab治疗比Docetaxel治疗\n可获得更长的中位整体生存率（Median OS: 13.8 vs. 9.6）。\n•\tPACIFIC Phase III：在不可切除且经过先期化疗的晚期NSCLC患者，接受Durvalumab治疗与安慰剂相比，能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n•\tPOPLAR Phase II：临床试验证明在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，使用Atezolizumab治疗比Docetaxel治疗，可获得更长中位持续响应期和整体生存期（Median DOR: 18.6 vs. 7.2; OS: 12.6 vs. 9.7）。\n•\tStudy 1108 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                       'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                       'medicine_note': medicine_note}
        #     1
        if ((realMSI == 'MSI-H'and mmr_mean == '异常') or (realMSI =='MSI-H' and mmr_mean == '正常') or ((realMSI =='MSI-S' or realMSI =='MSI-L') and mmr_mean == '异常')) and (tmb_mean == '低' or tmb_mean == '中'):
            Nivolumab_mean = RichText(
                '• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（CheckMate-026a）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，TMB低的晚期非小细胞肺癌肺癌患者接受Nivolumab治疗的中位无进展生存期比化疗更短（CheckMate 026c）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和良好的响应率,且PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（CheckMate-012a）；',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应（CheckMate-012b）；',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用,在2年整体生存率上高达62%。（CheckMate-012c）；',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（CheckMate-063）；',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞肺癌患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（CheckMate-057，CheckMate-017）；',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗可获得良好的治疗效果（NCT00730639）。',
                               style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（TPS>=50%），可以考虑在一线治疗中使用Pembrolizumab（KEYNOTE-024）；\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与Pemetrexed和Carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（KEYNOTE-021）；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrozulimab在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好(KEYNOTE-001a)；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add(
                '• FDA批准Pembrolizumab单药可用于治疗在铂类药物化疗后进展且PD-L1表达（TPS>=1%）的非小细胞肺癌患者（KEYNOTE-010）；\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add(
                '• FDA批准Prembrolizumab可用于前期治疗进展后没有可行的替代方案，且MSI-H或dMMR的无法手术切除或晚期转移性实体瘤患者（FDA批准适应症）；\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add(
                '• 临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（KEYNOTE-028）；\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add(
                '• 临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（KEYNOTE-001b）。',
                style="HLAMeanStyle")
            Atezolizumab_mean = RichText(
                '• 临床试验表明Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率（BIRCH）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• FDA批准在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，建议使用Atezolizumab进行后续治疗，且PD-L1在肿瘤细胞和浸润淋巴细胞中的表达水平与治疗疗效呈正相关（POPLAR）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• FDA批准在接受过先期治疗的非小细胞肺癌患者，可以考虑使用Atezolizumab进行后续治疗（OAK）。',
                style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab可作为不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC）；\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1表达高（TPS>=25%）的晚期非小细胞肺癌患者在接受Durvalumab治疗时，比PD-L1表达低或不表达的患者，存在明显的响应率和生存期获益（Study 1108）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ATLANTIC）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 非小细胞肺癌患者中正在开展的3个关于Durvalumab药物的三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC，MYSTIC，NEPTUNE）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者，旨在评估PD-L1高表达和PD-L1低表达分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tATLANTIC Phase II：临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ORR: 16.4% vs. 7.5%）。\n•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期NSCLC患者中，表现出良好的耐受性和响应率（ORR：26%-31%）。\n•\tCheckMate-012a Phase I：临床试验纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和高的响应率，PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（ORR: 47 vs. 38%; ORR with PD-L1 TPS≥1%: 57% vs. 57%）。\n•\tCheckMate-012b Phase I：临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应(Aes: 71%; ORR 23%; 6-month PFS: 41%; Median OS 19.4; 12-month and 18-month OS: 73% and 57%)。\n•\tCheckMate-012c Phase I：临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用虽然在AE导致的治疗终止率上比单药高，但在2年整体生存率上却达到了62%（ORR: 43%，24-month OS: 62%）。\n•\tCheckMate-017 Phase III：转移性鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n•\tCheckMate-026a Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。\n•\tCheckMate-026c Phase III：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n•\tCheckMate-057 Phase III：转移性非鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n•\tCheckMate-063 Phase II：临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（ORR: 14.5%; Adverse events: 17%）。\n•\tFDA批准适应症：根据KEYNOTE-016， KEYNOTE-164， KEYNOTE-012， KEYNOTE-028，KEYNOTE-158回溯性或/和前瞻性的临床试验结果，FDA批准Pembrolizumab用于治疗微卫星高度不稳定（MSI-H）/DNA错配修复基因缺失（dMMR）的实体瘤患者。\n•\tImpower 150 Phase III：临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时（64% VS 48%），明显降低了疾病进展和死亡的风险（PFS 8.3 vs. 6.4）。\n•\tKEYNOTE-001a Phase Ib：临床试验表明帕姆单抗在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好（PD-L1 TPS>=50% vs. ALL，ORR： 51% vs. 27%；12-month PFS： 54% vs. 35%；12-month OS： 85% vs. 71%）。\n•\tKEYNOTE-001b Phase Ib：临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（Median PFS: 4.4 vs. 2.1，Median PFS: 6.3 （颅外放射） vs. 2.0，Median OS: 10.7 vs. 5.3，Median OS: 11.6 vs. 5.3）。\n•\tKEYNOTE-010 Phase II/ III：在使用铂药化疗后进展且PD-L1表达（TPS >1%）的NSCLC患者中，接受Pembrolizumab治疗（10mg/kg每三周一次）比接受Docetaxel治疗，在生存期中位数上有110%的延长。\n•\tKEYNOTE-021 Phase II： 在非鳞性晚期NSCLC的一线治疗中Pembrolizumab、Pemetrexed和Carboplatin的联合用药是有效且可耐受的。三种药物的联合使用比仅使用化疗药物具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n•\tKEYNOTE-024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n•\tKEYNOTE-028 Phase Ib：临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（ORR: 33%）。\n•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tNCT00730639 Phase I：临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗在可控的安全范围内获得良好的中位整体生存期和整体生存率（Median OS: 9.9; 12-month OS: 42%; Adverse events: 14%）。\n•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tOAK Phase III：临床试验证明在先期治疗后的非小细胞肺癌患者中，使用Atezolizumab治疗比Docetaxel治疗,可获得更长的中位整体生存率（Median OS: 13.8 vs. 9.6）。\n•\tPACIFIC Phase III：在不可切除且经过先期化疗的晚期NSCLC患者，接受Durvalumab治疗与安慰剂相比，能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n•\tPOPLAR Phase II：临床试验证明在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，使用Atezolizumab治疗比Docetaxel治疗，可获得更长中位持续响应期和整体生存期（Median DOR: 18.6 vs. 7.2; OS: 12.6 vs. 9.7）。\n•\tStudy 1108 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。',
                style="HLAMeanStyle")

            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                       'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                       'medicine_note': medicine_note}
        # 3
        if ((realMSI == 'MSI-S' or realMSI == 'MSI-L')and mmr_mean =='正常') and tmb_mean =='高' :
            Nivolumab_mean = RichText(
                '• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（CheckMate-026a）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，TMB高的晚期非小细胞肺癌患者接受Nivolumab治疗比化疗可获得更长的无进展生存期（CheckMate-026b）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• CheckMate-227临床试验的初步结果表明，Nivolumab和ipilimumab联合用药可用于TMB高的非小细胞肺癌患者的一线治疗中（CheckMate-227）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验表明纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和良好的响应率,且PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（CheckMate-012a）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应（CheckMate-012b）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用,在2年整体生存率上高达62%。（CheckMate-012c）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（CheckMate-063）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• FDA批准转移性非小细胞肺癌患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（CheckMate-057，CheckMate-017）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，广泛期小细胞肺癌患者不论在接受Nivolumab联合Ipilimumab治疗，还是Nivolumab单药治疗中，TMB高的患者比TMB中和低的患者，在客观响应率和12个月生存率都有明显提升（CheckMate-032）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗可获得良好的治疗效果（NCT00730639）。',
                style="HLAMeanStyle")

            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（TPS>=50%），可以考虑在一线治疗中使用Pembrolizumab（KEYNOTE-024）；\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与Pemetrexed和Carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（KEYNOTE-021）；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrozulimab在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好(KEYNOTE-001a)；',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于治疗在铂类药物化疗后进展且PD-L1表达（TPS>=1%）的非小细胞肺癌患者（KEYNOTE-010）；',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（KEYNOTE-028）；',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（KEYNOTE-001b）。',
                                   style="HLAMeanStyle")
            Atezolizumab_mean = RichText(
                '• 临床试验表明Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率（BIRCH）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• FDA批准在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，建议使用Atezolizumab进行后续治疗，且PD-L1在肿瘤细胞和浸润淋巴细胞中的表达水平与治疗疗效呈正相关（POPLAR）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• FDA批准在接受过先期治疗的非小细胞肺癌患者，可以考虑使用Atezolizumab进行后续治疗（OAK）。',
                                  style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab可作为不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC）；\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1表达高（TPS>=25%）的晚期非小细胞肺癌患者在接受Durvalumab治疗时，比PD-L1表达低或不表达的患者，存在明显的响应率和生存期获益（Study 1108）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ATLANTIC）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 非小细胞肺癌患者中正在开展的3个关于Durvalumab药物的三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC，MYSTIC，NEPTUNE）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者，旨在评估PD-L1高表达和PD-L1低表达分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tATLANTIC Phase II：临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ORR: 16.4% vs. 7.5%）。\n•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期NSCLC患者中，表现出良好的耐受性和响应率（ORR：26%-31%）。\n•\tCheckMate-012a Phase I：临床试验纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和高的响应率，PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（ORR: 47 vs. 38%; ORR with PD-L1 TPS≥1%: 57% vs. 57%）。\n•\tCheckMate-012b Phase I：临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应(Aes: 71%; ORR 23%; 6-month PFS: 41%; Median OS 19.4; 12-month and 18-month OS: 73% and 57%)。\n•\tCheckMate-012c Phase I：临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用虽然在AE导致的治疗终止率上比单药高，但在2年整体生存率上却达到了62%（ORR: 43%，24-month OS: 62%）。\n•\tCheckMate-017 Phase III：转移性鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n•\tCheckMate-026a Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。\n•\tCheckMate-026b Phase III：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n•\tCheckMate-032 Phase I/II：Nivolumab单药治疗，以及Nivolumab与Ipilimumab联合治疗在接受过治疗的广泛期小细胞肺癌患者中表现出持久的抗肿瘤活性和可控的安全性，TMB高的SCLC患者比TMB低的患者，客观响应率和1年期生存率都有明显提升（ORR: 46% vs. 16%; 1-year OS: 62% vs. 20%）。\n•\tCheckMate-057 Phase III：转移性非鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n•\tCheckMate-063 Phase II：临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（ORR: 14.5%; Adverse events: 17%）。\n•\tCheckMate-227 Phase III ：CheckMate-227临床试验的初步结果表明在晚期非小细胞肺癌患者的一线治疗中，如果患者TMB高，则使用Nivolumab和ipilimumab联合用药比化疗可获得更长的无进展生存期（Median PFS: 9.7 vs. 5.8）。\n•\tImpower 150 Phase III：临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时（64% VS 48%），明显降低了疾病进展和死亡的风险（PFS 8.3 vs. 6.4）。\n•\tKEYNOTE-001a Phase Ib：临床试验表明帕姆单抗在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好（PD-L1 TPS>=50% vs. ALL，ORR： 51% vs. 27%；12-month PFS： 54% vs. 35%；12-month OS： 85% vs. 71%）。\n•\tKEYNOTE-001b Phase Ib：临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（Median PFS: 4.4 vs. 2.1，Median PFS: 6.3 （颅外放射） vs. 2.0，Median OS: 10.7 vs. 5.3，Median OS: 11.6 vs. 5.3）。\n•\tKEYNOTE-010 Phase II/ III：在使用铂药化疗后进展且PD-L1表达（TPS >1%）的NSCLC患者中，接受Pembrolizumab治疗（10mg/kg每三周一次）比接受Docetaxel治疗，在生存期中位数上有110%的延长。\n•\tKEYNOTE-021 Phase II： 在非鳞性晚期NSCLC的一线治疗中Pembrolizumab、Pemetrexed和Carboplatin的联合用药是有效且可耐受的。三种药物的联合使用比仅使用化疗药物具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n•\tKEYNOTE-024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n•\tKEYNOTE-028 Phase Ib：临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（ORR: 33%）。\n•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tNCT00730639 Phase I：临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗在可控的安全范围内获得良好的中位整体生存期和整体生存率（Median OS: 9.9; 12-month OS: 42%; Adverse events: 14%）。\n•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tOAK Phase III：临床试验证明在先期治疗后的非小细胞肺癌患者中，使用Atezolizumab治疗比Docetaxel治疗,可获得更长的中位整体生存率（Median OS: 13.8 vs. 9.6）。\n•\tPACIFIC Phase III：在不可切除且经过先期化疗的晚期NSCLC患者，接受Durvalumab治疗与安慰剂相比，能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n•\tPOPLAR Phase II：临床试验证明在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，使用Atezolizumab治疗比Docetaxel治疗，可获得更长中位持续响应期和整体生存期（Median DOR: 18.6 vs. 7.2; OS: 12.6 vs. 9.7）。\n•\tStudy 1108 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                       'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                       'medicine_note': medicine_note}
            # 2
        if ((realMSI == 'MSI-S' or realMSI =='MSI-L') and mmr_mean =='正常') and (tmb_mean == '低' or tmb_mean == '中'):
            Nivolumab_mean = RichText(
                '• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（CheckMate-026a）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，TMB低的晚期非小细胞肺癌肺癌患者接受Nivolumab治疗的中位无进展生存期比化疗更短（CheckMate 026c）；\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和良好的响应率,且PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（CheckMate-012a）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应（CheckMate-012b）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用,在2年整体生存率上高达62%。（CheckMate-012c）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（CheckMate-063）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞肺癌患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（CheckMate-057，CheckMate-017）；\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗可获得良好的治疗效果（NCT00730639）。',
                               style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（TPS>=50%），可以考虑在一线治疗中使用Pembrolizumab（KEYNOTE-024）；\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与Pemetrexed和Carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（KEYNOTE-021）；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrozulimab在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好(KEYNOTE-001a)；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于治疗在铂类药物化疗后进展且PD-L1表达（TPS>=1%）的非小细胞肺癌患者（KEYNOTE-010）；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（KEYNOTE-028）；\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（KEYNOTE-001b）。',
                                   style="HLAMeanStyle")
            Atezolizumab_mean = RichText(
                '• 临床试验表明Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率（BIRCH）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• FDA批准在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，建议使用Atezolizumab进行后续治疗，且PD-L1在肿瘤细胞和浸润淋巴细胞中的表达水平与治疗疗效呈正相关（POPLAR）；\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• FDA批准在接受过先期治疗的非小细胞肺癌患者，可以考虑使用Atezolizumab进行后续治疗（OAK）。',
                style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab可作为不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC）；\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1表达高（TPS>=25%）的晚期非小细胞肺癌患者在接受Durvalumab治疗时，比PD-L1表达低或不表达的患者，存在明显的响应率和生存期获益（Study 1108）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ATLANTIC）；\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 非小细胞肺癌患者中正在开展的3个关于Durvalumab药物的三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC，MYSTIC，NEPTUNE）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者，旨在评估PD-L1高表达和PD-L1低表达分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tATLANTIC Phase II：临床试验表明使用Durvalumab对未检测到EGFR/ALK突变，且接受过二线以上系统性治疗后失败的晚期非小细胞肺癌患者的治疗中，PD-L1阳性患者比PD-L1阴性患者具有更高的响应率（ORR: 16.4% vs. 7.5%）。\n•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选（TC3，IC3）的晚期NSCLC患者中，表现出良好的耐受性和响应率（ORR：26%-31%）。\n•\tCheckMate-012a Phase I：临床试验纳武单抗和伊匹单抗联合用药在晚期非小细胞肺癌的一线治疗中，表现出持久的响应和高的响应率，PD-L1 TPS>=1%患者与整体相比表现出较高的响应率（ORR: 47 vs. 38%; ORR with PD-L1 TPS≥1%: 57% vs. 57%）。\n•\tCheckMate-012b Phase I：临床试验表明纳武单抗单药在晚期非小细胞肺癌一线治疗中表现出可耐受的安全性和持久的响应(Aes: 71%; ORR 23%; 6-month PFS: 41%; Median OS 19.4; 12-month and 18-month OS: 73% and 57%)。\n•\tCheckMate-012c Phase I：临床试验表明纳武单抗与含铂两药化疗（PT-DC）联用虽然在AE导致的治疗终止率上比单药高，但在2年整体生存率上却达到了62%（ORR: 43%，24-month OS: 62%）。\n•\tCheckMate-017 Phase III：转移性鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n•\tCheckMate-026a Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。\n•\tCheckMate-026c Phase III：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n•\tCheckMate-057 Phase III：转移性非鳞性NSCLC患者接受Nivolumab单药治疗比接受Docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n•\tCheckMate-063 Phase II：临床试验表明在晚期难治鳞状非小细胞肺癌患者中，使用Nivolumab在可控安全范围内获得良好的疗效（ORR: 14.5%; Adverse events: 17%）。\n•\tImpower 150 Phase III：临床试验表明Atezolizumab、Bevacizumab与化疗的三联组合疗法比Bevacizumab和化疗的联合治疗，在晚期非小细胞肺癌患者的一线治疗中，提高有效率的同时（64% VS 48%），明显降低了疾病进展和死亡的风险（PFS 8.3 vs. 6.4）。\n•\tKEYNOTE-001a Phase Ib：临床试验表明帕姆单抗在未经治疗（treatment-naive），PD-L1表达的晚期非小细胞肺癌治疗中，取得了长期的整体生存率获益和可控的安全指征，尤其是PD-L1 TPS>=50%的患者中治疗效果更好（PD-L1 TPS>=50% vs. ALL，ORR： 51% vs. 27%；12-month PFS： 54% vs. 35%；12-month OS： 85% vs. 71%）。\n•\tKEYNOTE-001b Phase Ib：临床试验显示先期放疗的帕姆单抗治疗的晚期非小细胞肺癌患者与先期未经放疗的帕姆单抗治疗的晚期非小细胞肺癌患者相比，具有更长的无进展生存期和整体生存期（Median PFS: 4.4 vs. 2.1，Median PFS: 6.3 （颅外放射） vs. 2.0，Median OS: 10.7 vs. 5.3，Median OS: 11.6 vs. 5.3）。\n•\tKEYNOTE-010 Phase II/ III：在使用铂药化疗后进展且PD-L1表达（TPS >1%）的NSCLC患者中，接受Pembrolizumab治疗（10mg/kg每三周一次）比接受Docetaxel治疗，在生存期中位数上有110%的延长。\n•\tKEYNOTE-021 Phase II： 在非鳞性晚期NSCLC的一线治疗中Pembrolizumab、Pemetrexed和Carboplatin的联合用药是有效且可耐受的。三种药物的联合使用比仅使用化疗药物具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n•\tKEYNOTE-024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n•\tKEYNOTE-028 Phase Ib：临床试验表明Pembrolizumab在PD-L1阳性，有过先期治疗的广泛期小细胞肺癌治疗中的安全性可控，且获得了33%的整体响应率（ORR: 33%）。\n•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tNCT00730639 Phase I：临床试验表明在过度治疗的非小细胞肺癌患者中，使用Nivolumab治疗在可控的安全范围内获得良好的中位整体生存期和整体生存率（Median OS: 9.9; 12-month OS: 42%; Adverse events: 14%）。\n•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前该临床试验正在开展中。\n•\tOAK Phase III：临床试验证明在先期治疗后的非小细胞肺癌患者中，使用Atezolizumab治疗比Docetaxel治疗,可获得更长的中位整体生存率（Median OS: 13.8 vs. 9.6）。\n•\tPACIFIC Phase III：在不可切除且经过先期化疗的晚期NSCLC患者，接受Durvalumab治疗与安慰剂相比，能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n•\tPOPLAR Phase II：临床试验证明在铂类化疗药物治疗期间或治疗之后疾病进展的非小细胞肺癌患者，使用Atezolizumab治疗比Docetaxel治疗，可获得更长中位持续响应期和整体生存期（Median DOR: 18.6 vs. 7.2; OS: 12.6 vs. 9.7）。\n•\tStudy 1108 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                   'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                   'medicine_note': medicine_note}
        #     4

        # else:
        #     Nivolumab_mean = RichText('未知',style="HLAMeanStyle")
        #     Pembrolizumab_mean = RichText('未知',style="HLAMeanStyle")
        #     Atezolizumab_mean = RichText('未知',style = "HLAMeanStyle")
        #     Durvalumab_mean = RichText('未知',style="HLAMeanStyle")
        #     medicine_note = RichText('未知',style="HLAMeanStyle")
        #     context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
        #                'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
        #                'medicine_note': medicine_note}
        # print (context)
        #     6
    def seqplatform(self):
        global realtestplatform
        global context
        gene_num = 0
        cover_region=0
        if realtestplatform == 'Hiseq':
            gene_num="21000"
            cover_region="39,000,000bp"
        if realtestplatform=='CN500':
            gene_num="21000"
            cover_region="35,000,000bp"
        if realtestplatform=='NovelSeq':
            gene_num="21000"
            cover_region="35,000,000bp"
        context = {'gene_num':gene_num,'cover_region':cover_region}
        # print (context)

    def msiinfor(self):
        global context
        global realBAT_25
        global realBAT_26
        global realNR_21
        global realNR_24
        global realMONO_27
        context ={'BAT_25':realBAT_25,'BAT_26':realBAT_26,'NR_21':realNR_21,'NR_24':realNR_24,'MONO_27':realMONO_27}


    def run(self):
        content ={}
        global context
        BasicInfoName = self.kwargs.get('Basic_InfoName')
        MSIPathName = self.kwargs.get('MSI_PathName')
        ResultFileName = self.kwargs.get('Result_FileName')
        OutPathName =self.kwargs.get('Out_PathName')
        # print (OutPathName)
        ResultFileInst = FileIter(ResultFileName)
        for ResultItem in ResultFileInst:
            # print (ResultItem)
            if "SAMPLEID" in ResultItem:
                global SAMPLEID
                SAMPLEID= ResultItem[1]
            if "SNV" in ResultItem:
                SNV= ResultItem[1]
            if "Indel" in ResultItem:
                Indel = ResultItem[1]
            if "CNV" in ResultItem:
                CNV = ResultItem[1]
            if "SV" in ResultItem:
                SV = ResultItem[1]
            if "MMR" in ResultItem:
                MMR = ResultItem[1]
            if "POL" in ResultItem:
                POL = ResultItem[1]
            if "HLA" in ResultItem:
                HLA =ResultItem[1]
            if "MSI" in ResultItem:
                MSI = ResultItem[1]
            if "TMB" in ResultItem:
                TMB = ResultItem[1]
            if "NEO" in ResultItem:
                NEO = ResultItem[1]
            if "NEO_list" in ResultItem:
                NEO_list = ResultItem[1]
            if "QC" in ResultItem:
                QC = ResultItem[1]
            if "Pathway" in ResultItem:
                Pathway = ResultItem[1]
        # print (CNV)
        SNVInst = FileIter(SNV)
        IndelInst = FileIter(Indel)
        CNVInst = FileIter(CNV)
        NeoInst = FileIter(NEO_list)
        MMRInst = FileIter(MMR)
        POLInst = FileIter(POL)
        context={}
        self.autotable(SNVInst,IndelInst,CNVInst,MMRInst,POLInst,NeoInst)
        content.update(context)
        self.fill_basicinfo(BasicInfoName)
        content.update(context)
        self.fill_msiimage(MSIPathName)
        content.update(context)
        self.fillqc(QC)
        content.update(context)
        self.fillpathway(Pathway)
        content.update(context)
        context = self.checkPoint(TMB, NEO, MMR, POL)
        content .update(context)
        context = self.HLA(HLA)
        content.update(context)
        self.medication()
        content.update(context)
        self.seqplatform()
        content.update(context)
        self.msiinfor()
        content.update(context)
        doc.render(content)
        # doc.save("/disk/lulu/autoreport/output/generated_doc.docx")  # 保存
        doc.save(OutPathName)

    def autotable(self, inputInst0, inputInst1, inputInst2,inputInst3, inputInst4, inputInst5):
            global context
         # if not context:
            context = {'tbl_contents': [],'indel_contents':[],'cnv_contents':[],'cnv_contents1':[],'MMR_contents':[],'POL_contents':[],'Neo_contents':[], 'sv_contents':[],}

            for InputItem in inputInst0:
                context['tbl_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], InputItem[5]]})
            for InputItem in inputInst1:
                context['indel_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], InputItem[5]]})
            for InputItem in inputInst2:
                if InputItem[1] == "GAIN":
                    context['cnv_contents'].append({'value': [InputItem[0], "增加", InputItem[2]]})
                elif InputItem[1] == "DELETION":
                    context['cnv_contents1'].append({'value': [InputItem[0], "减少", InputItem[2]]})
            for InputItem in inputInst3:
                context['MMR_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4]]})
            for InputItem in inputInst4:
                context['POL_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4]]})
            for InputItem in inputInst5:
                if InputItem[5]=="0":
                    context['Neo_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], "NA"]})
                else:
                    context['Neo_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4], InputItem[5]]})
            # for InputItem in inputInst6:
            #     context['sv_contents'].append({'value': [InputItem[0], InputItem[1], InputItem[2]]})
            # print (context)



        #当然，这个包的功能远远不止上面例子中的一些，可以包含图片
        # myimage = InlineImage(doc, 'test_files/python_logo.png', width=Mm(20))  # tpl便是上面例子中的doc对象也可以包含另一个docx文档，
        # sub = doc.new_subdoc()
        # sub.subdocx = Document('d:\\2.docx').
        # doc.render({'sub': sub})



def param(argv):
    # global CNV_File
    # global SNV_File
    # global Indel_File
    # # global Prefix
    # # global Draw_Path
    global Basic_Info
    global MSI_Path
    global Result_File
    global Out_Path
    # # global HLA_File
    # global Neo_File
    # global MMR_File
    # global POL_File
    # global Gene_Data
    # global Road_Path
    try:
        # options, args = getopt.getopt(argv, "hC:S:I:N:M:P:B:",
        #     ["help", "CNV_File=", "SNV_File=", "Indel_File=", "Neo_File=", "MMR_File=", "POL_File=", "Basic_Info="])
        # # options, args = getopt.getopt(argv, "hC:S:I:P:M:B:H:N:G:R", ["help", "CNV_File=", "SNV_File=", "Indel_File=","Prefix=","Draw_Path=","Basic_Info=","HLA_File=","Neo_File=","Gene_Data=","Road_Path="])
        options, args = getopt.getopt(argv, "hB:M:R:O:",["help", "Basic_Info=", "MSI_Path=", "Result_File=","Out_Path="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for option, value in options:
        if not option:
            usage()
        if option in ("-B","--Basic_Info"):
            Basic_Info = value
        if option in ("-M", "--MSI_Path"):
            MSI_Path = value
        if option in ("-R", "Result_File"):
            Result_File = value
        if option in ("-O","Out_Path"):
            Out_Path=value
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
        -B(--Basic_Info) Basic_Info File whic contains the information of patient
        -M(--MSI_Path) the path of the MSI image
        -P(--POL_File) POL FILE
        -R(--Result_File) the Result PATH from the process result 
        -O(--Out_Path) the outputpath
        ''')


def cmdDict():
    global Basic_Info
    global MSI_Path
    global Result_File
    global Out_Path
    callerDict = {
        'Basic_InfoName': Basic_Info,
        'MSI_PathName': MSI_Path,
        'Result_FileName': Result_File,
        'Out_PathName':Out_Path,
    }
    return callerDict


if __name__ == '__main__':
    Basic_Info = "" #患者基本信息以及MSI图路径的配置文件（csv配置文件）
    MSI_Path = "" #MSI图的路径
    Result_File = "" #流程给出的结果路径文件
    Out_Path = ""
    if len(sys.argv) < 2:
        print ('please input parameters! or You can input "--help" to get the usage')
        sys.exit()
    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        # print (callerDict)
        # print callerDict
        inst = allCallerSimple(**callerDict)
        inst.run()

