# !/usr/bin/python
# -*- coding: utf-8 -*-
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

##此版本是整合了所有功能模块的完整合集。

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
        global tnb_mean
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
            tnb_mean = line[2]
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
        if tmb_result >= 9:
            tmb_mean = '高'
        elif tmb_result < 3:
            tmb_mean = '低'
        else:
            tmb_mean = '中'
        #
        if nonsys_num >= 248:
            nonsys_mean = '高'
            tmb_des = "本检测得到的TMB结果高于平均值"
            tmb_status = "TMB-H(>248个非同义突变位点)"
        elif nonsys_num < 143:
            nonsys_mean = '低'
            tmb_des = "本检测得到的TMB结果低于平均值"
            tmb_status = "TMB-L(0-143个非同义突变位点)"
        else:
            nonsys_mean = '中'
            tmb_des = "本检测得到的TMB结果位于中位数附近"
            tmb_status = "TMB-M(143-248个非同义突变位点)"
        #
        if sys_num >= 100:
            sys_mean = '高'
        elif sys_num < 57:
            sys_mean = '低'
        else:
            sys_mean = '中'
        #
        if kaks == 'N/A':
            kaks_mean = 'N/A'
            kaks_des = RichText('')
        elif kaks >= 3:
            kaks_mean = '较高'
            kaks_des = RichText('\n＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio大于等于3.0，反映样本中的肿瘤细胞的增殖能力处于较高状态；',style='HLAMeanStyle')
        elif kaks < 2.5:
            kaks_mean = '较低'
            kaks_des = RichText('\n＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio小于2.5，反映样本中的肿瘤细胞的增殖能力处于较低状态；',style='HLAMeanStyle')
        else:
            kaks_mean = '中性'
            kaks_des = RichText('\n＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio大于等于2.5小于3.0，反映样本中的肿瘤细胞的增殖能力处于中性状态；',style='HLAMeanStyle')
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
            'tnb_mean':tnb_mean,
            'tmb_des': tmb_des,
            'tmb_status': tmb_status
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
            mean.add('et al., Science）', italic=True,style = "HLAMeanStyle")
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
            print (line[1])
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
        global context
        global given_id
        global SAMPLEID
        global realMSI
        given_id=  SAMPLEID
        # 样品名，可以作为该函数的参数进行传入。传入之前可以根据随意一个输出文件的名字来得到。
        for row in reader:
            print (row)
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
        print (realmedi_history)
        print (realdiagnose)
        print (realMSI)
        csvFile.close()
        context = {'name': realName, 'sex': realsex, 'age': realage, 'tel': realtel, 'send_hospital': realsend_hospital,
                   'send_doctor': realsend_doctor, 'send_sample': realsend_sample,
                   'send_date': realsend_date, 'diagnose_agency': realdiagnose_agency,
                   'diagnose':realdiagnose, 'stage': realstage, 'medi_history': realmedi_history,
                   'test_item':realtest_item, 'receive_date': realreceive_date, 'sample_id': given_id,
                   'report_date': date_today, 'DNAng': realDNAng}
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
        print (realMSI)
        print (mmr_mean)
        print (tmb_mean)
        print (tnb_mean)
        if (realMSI == 'MSI-H'or mmr_mean =='异常') and tmb_mean == '高' and tnb_mean == '低':
            Nivolumab_mean = RichText('• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（Checkmate 026）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 最新临床试验后的探索性研究数据显示，TMB高的晚期非小细胞肺癌患者接受Nivolumab治疗比化疗可获得更长的无进展生存期（Checkmate 026）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（Checkmate 057，Checkmate 017）。\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性结直肠癌患者在化疗无效或进展后，在二线治疗中建议使用Nivolumab（Checkmate 142）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 研究表明TMB高的患者与接受Nivolumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验CheckMate 032结果表明，TMB高的小细胞肺癌患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升。与临床试验Checkmate 026非小细胞肺癌研究的横向对比发现，虽然两者亚型不同，但在TMB高、中、低的划分指标上却相当。这两个临床试验相互印证了TMB高的群体更容易从Nivolumab治疗中获益（Checkmate 032）。',
                style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（>=50%），可以考虑在一线治疗中使用Pembrolizumab（Keynote 024）。\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与pemetrexed和carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（Keynote 021）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于PD-L1表达（TPS>=1%）的晚期非小细胞肺癌，在铂类药物化疗进展的二线治疗中（Keynote 010）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 2017年，FDA批准Prembrolizumab可用于治疗MSI-H或dMMR的无法手术切除或晚期转移性实体瘤患者（前期治疗进站后没有可行的替代方案，FDA批准适应症）\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 研究表明TMB高的患者与接受Pembrolizumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。',
                style="HLAMeanStyle")
            Atezolizumab_mean = RichText('• 临床试验表明Atezolizumab在经过PD-L1表达筛选的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（BIRCH Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明与单独Bevacizumab与化疗相比，Atezolizumab、Bevacizumab与化疗的三联组合疗法一线用于晚期非小细胞肺癌患者治疗，在提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150 Phase III）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• NCCN指南推荐在转移性非小细胞患者在铂类化药治疗无效或进展后，特别是对于检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者，可以在二线治疗中使用Atezolizumab（POPLAR Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• 研究表明TMB水平与Atezolizumab临床治疗效果呈正相关（10.1016/j.jtho.2016.11.343）。',
                                  style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab用于不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC Phase III）。\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1高（>=25%）的晚期NSCLC患者，接受Durvalumab治疗比PD-L1低或不表达的患者存在明显的响应率和生存期获益（NCT01693562）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性非小细胞肺癌患者，可明显提升患者的响应率（ATLANTIC Phase II）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 正在开展的三个Durvalumab三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC Phase III，MYSTIC Phase III，NEPTUNE Phase III）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tCheckmate 026 Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。Checkmate 026 Phase III回溯性研究：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中相比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 057 Phase III：转移非鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 017 Phase III：转移鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 142 Phase II：经过前期治疗的转移性NSCLC患者，如果存在DNA错配修复基因缺失（dMMR）或微卫星高度不稳定（MSI-H），接受Nivolumab治疗的响应率可达到32.7%。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1200/JCO.2016.34.15_suppl.9017：研究表明接受Nivolumab/pembrolizumab/avelumab治疗的晚期非小细胞肺癌患者，TMB高的群体具有更长的治疗耐受时间（Median time on anti-PD-1/PD-L1 therapy: 64 weeks vs. 17 weeks）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckMate 032 Phase I/II：Nivolumab单药治疗，以及Nivolumab与ipilimumab联合治疗在以前接受过治疗的小细胞肺癌患者中表现出抗肿瘤活性的持久的响应和可控的安全性，TMB高的SCLC患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升（ORR: 46% vs. 16%; 1-year OS: 62% vs. 20%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗将比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 021 Phase II： 帕姆单抗和卡铂、培美曲塞的联合用药在非鳞性晚期NSCLC的一线治疗中是有效且耐受的。三种药物的联合使用将比仅化疗药物使用具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 010 Phase II/ III：在使用铂药基础的化疗治疗后进展的NSCLC患者中，如果存在PD-L1表达（TPS >1%），接受Pembrolizumab治疗（10mg/kg每三周一次）的患者比接受多西他赛治疗的患者在生存期中位数上有110%的延长；\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tFDA批准适应症：根据Keynote 016， Keynote 164， Keynote 012， Keynote 028，Keynote 158回溯性或/和前瞻性的临床试验结果，FDA批准pembrolizumab可用于治疗微卫星高度不稳定（MSI-H）/DNA错配修复基因缺失（dMMR）的实体瘤患者。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选的晚期NSCLC患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（ORR 18%-22%，26%-31% TC3 IC3）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tImpower 150 Phase III：根据临床试验结果，Atezolizumab、Bevacizumab与化疗，三联组合疗法一线用于晚期肺癌患者，与Bevacizumab和化疗相比，有效率更高（64% VS 48%），可降低38%的疾病进展和死亡风险（PFS 8.3 vs. 6.4），有望提高患者生存期。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPOPLAR Phase II：在使用铂药基础的化疗治疗后进展的NSCLC患者中，接受Atezolizumab治疗的患者比接受多西他赛治疗的患者在总体生存期上有30%的延长；根据2018第二版NCCN NSCLC专家指南，使用Nivolumab和Atezolizumab无需进行PD-L1免疫组化检测，但根据POPLAR II期临床试验的结果，检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者（TC3 or IC3）总体的生存期或更高。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1016/j.jtho.2016.11.343：研究表明不论PD-L1表达筛选与否，晚期NSCLC患者中TMB较高的群体，在Atezolizumab用药有效率上有明显提升（ORR：28% vs. 13%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPACIFIC Phase III：在连续使用铂药基础的放化疗治疗2个以上周期的未进展NSCLC患者，接受Durvalumab治疗的患者比安慰剂组患者能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNCT01693562 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tATLANTIC Phase II：根据临床试验结果，采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性NSCLC患者，与PD-L1阴性患者相比，明显提升了患者的响应率（ORR: 16.4% vs. 7.5%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在评估PD-L1-high和PD-L1-low分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，与Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                       'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                       'medicine_note': medicine_note}
        #     1
        if (realMSI == 'MSI-H'or mmr_mean == '异常') and tmb_mean == '高' and tnb_mean =='高':
            Nivolumab_mean = RichText(
                '• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（Checkmate 026）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，TMB高的晚期非小细胞肺癌患者接受Nivolumab治疗比化疗可获得更长的无进展生存期（Checkmate 026）。根据Nature两篇文献的回溯性研究报道，新抗原“fitness”模型中high-fitness患者群体更容易从免疫检查点抑制剂治疗中获益（10.1038/nature24462，10.1038/nature24473）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（Checkmate 057，Checkmate 017）。\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• FDA批准转移性结直肠癌患者在化疗无效或进展后，在二线治疗中建议使用Nivolumab（Checkmate 142）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 研究表明TMB高的患者与接受Nivolumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验CheckMate 032结果表明，TMB高的小细胞肺癌患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升。与临床试验Checkmate 026非小细胞肺癌研究的横向对比发现，虽然两者亚型不同，但在TMB高、中、低的划分指标上却相当。这两个临床试验相互印证了TMB高的群体更容易从Nivolumab治疗中获益（Checkmate 032）。',
                style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（>=50%），可以考虑在一线治疗中使用Pembrolizumab（Keynote 024）。\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与pemetrexed和carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（Keynote 021）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于PD-L1表达（TPS>=1%）的晚期非小细胞肺癌，在铂类药物化疗进展的二线治疗中（Keynote 010）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add(
                '• 2017年，FDA批准Prembrolizumab可用于治疗MSI-H或dMMR的无法手术切除或晚期转移性实体瘤患者（前期治疗进站后没有可行的替代方案，FDA批准适应症）。\n',
                style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 研究表明TMB高的患者与接受Pembrolizumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。根据Nature两篇文献的回溯性研究报道，新抗原“fitness”模型中high-fitness患者群体更容易从免疫检查点抑制剂治疗中获益（10.1038/nature24462，10.1038/nature24473）。',
                                   style="HLAMeanStyle")
            Atezolizumab_mean = RichText(
                '• 临床试验表明Atezolizumab在经过PD-L1表达筛选的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（BIRCH Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明与单独Bevacizumab与化疗相比，Atezolizumab、Bevacizumab与化疗的三联组合疗法一线用于晚期非小细胞肺癌患者治疗，在提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150 Phase III）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• NCCN指南推荐在转移性非小细胞患者在铂类化药治疗无效或进展后，特别是对于检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者，可以在二线治疗中使用Atezolizumab（POPLAR Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• 研究表明TMB水平与Atezolizumab临床治疗效果呈正相关（10.1016/j.jtho.2016.11.343）。',
                                  style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab用于不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC Phase III）。\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1高（>=25%）的晚期NSCLC患者，接受Durvalumab治疗比PD-L1低或不表达的患者存在明显的响应率和生存期获益（NCT01693562）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性非小细胞肺癌患者，可明显提升患者的响应率（ATLANTIC Phase II）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 正在开展的三个Durvalumab三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC Phase III， MYSTIC Phase III，NEPTUNE Phase III）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tCheckmate 026 Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。Checkmate 026 Phase III回溯性研究：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中相比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1038/nature24462：新抗原质量预测模型（fitness model）显示，新抗原质量而非新抗原数量可以作为胰腺导管腺癌预后的分子标记，新抗原质量高的患者群体具有较好的预后生存状况。新抗原质量预测模型与传统的新抗原数量预测模型的区别在于，在传统数量预测的基础上，加入了新抗原展示区分度和致病有效性的权重评分。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1038/nature24473：回溯性研究表明（其中包括在肺癌中的anti-PD-1治疗）新抗原质量预测模型（fitness model）可以预测免疫检查点抑制剂的治疗响应。高-fitness与低-finess相比，具有较好的治疗预后。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 057 Phase III：转移非鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 017 Phase III：转移鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 142 Phase II：经过前期治疗的转移性NSCLC患者，如果存在DNA错配修复基因缺失（dMMR）或微卫星高度不稳定（MSI-H），接受Nivolumab治疗的响应率可达到32.7%。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1200/JCO.2016.34.15_suppl.9017：研究表明接受Nivolumab/pembrolizumab/avelumab治疗的晚期非小细胞肺癌患者，TMB高的群体具有更长的治疗耐受时间（Median time on anti-PD-1/PD-L1 therapy: 64周 vs. 17周）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckMate 032 Phase I/II：Nivolumab单药治疗，以及Nivolumab与ipilimumab联合治疗在以前接受过治疗的小细胞肺癌患者中表现出抗肿瘤活性的持久的响应和可控的安全性，TMB高的SCLC患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升（ORR: 46% vs. 16%; 1-year OS: 62% vs. 20%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗将比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 021 Phase II： 帕姆单抗和卡铂、培美曲塞的联合用药在非鳞性晚期NSCLC的一线治疗中是有效且耐受的。三种药物的联合使用将比仅化疗药物使用具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 010 Phase II/ III：在使用铂药基础的化疗治疗后进展的NSCLC患者中，如果存在PD-L1表达（TPS >1%），接受Pembrolizumab治疗（10mg/kg每三周一次）的患者比接受多西他赛治疗的患者在生存期中位数上有110%的延长；\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tFDA批准适应症：根据Keynote 016， Keynote 164， Keynote 012， Keynote 028，Keynote 158回溯性或/和前瞻性的临床试验结果，FDA批准pembrolizumab可用于治疗微卫星高度不稳定（MSI-H）/DNA错配修复基因缺失（dMMR）的实体瘤患者。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选的晚期NSCLC患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（ORR 18%-22%，26%-31% TC3 IC3）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tImpower 150 Phase III：根据临床试验结果，Atezolizumab、Bevacizumab与化疗，三联组合疗法一线用于晚期肺癌患者，与Bevacizumab和化疗相比，有效率更高（64% VS 48%），可降低38%的疾病进展和死亡风险（PFS 8.3 vs. 6.4），有望提高患者生存期。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPOPLAR Phase II：在使用铂药基础的化疗治疗后进展的NSCLC患者中，接受Atezolizumab治疗的患者比接受多西他赛治疗的患者在总体生存期上有30%的延长；根据2018第二版NCCN NSCLC专家指南，使用Nivolumab和Atezolizumab无需进行PD-L1免疫组化检测，但根据POPLAR II期临床试验的结果，检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者（TC3 or IC3）总体的生存期或更高。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1016/j.jtho.2016.11.343：研究表明不论PD-L1表达筛选与否，晚期NSCLC患者中TMB较高的群体，在Atezolizumab用药有效率上有明显提升（ORR：28% vs. 13%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPACIFIC Phase III：在连续使用铂药基础的放化疗治疗2个以上周期的未进展NSCLC患者，接受Durvalumab治疗的患者比安慰剂组患者能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNCT01693562 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tATLANTIC Phase II：根据临床试验结果，采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性NSCLC患者，与PD-L1阴性患者相比，明显提升了患者的响应率（ORR: 16.4% vs. 7.5%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在评估PD-L1-high和PD-L1-low分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，与Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                       'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                       'medicine_note': medicine_note}
        # 3
        if realMSI == 'MSI-S'and mmr_mean =='正常' and tmb_mean =='高' and tnb_mean =='低':
            Nivolumab_mean = RichText(
                '• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（Checkmate 026）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，TMB高的晚期非小细胞肺癌患者接受Nivolumab治疗比化疗可获得更长的无进展生存期（Checkmate 026）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（Checkmate 057，Checkmate 017）。\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 研究表明TMB高的患者与接受Nivolumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 临床试验CheckMate 032结果表明，TMB高的小细胞肺癌患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率ORR和1年期生存率都有明显提升。与临床试验Checkmate 026非小细胞肺癌研究的横向对比发现，虽然两者亚型不同，但在TMB高、中、低的划分指标上却相当。这两个临床试验相互印证了TMB高的群体更容易从Nivolumab治疗中获益（Checkmate 032）。',
                style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（>=50%），可以考虑在一线治疗中使用Pembrolizumab（Keynote 024）。\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与pemetrexed和carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（Keynote 021）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于PD-L1表达（TPS>=1%）的晚期非小细胞肺癌，在铂类药物化疗进展的二线治疗中（Keynote 010）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add(
                '• 研究表明TMB高的患者与接受Pembrolizumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。',
                style="HLAMeanStyle")
            Atezolizumab_mean = RichText(
                '• 临床试验表明Atezolizumab在经过PD-L1表达筛选的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（BIRCH Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明与单独Bevacizumab与化疗相比，Atezolizumab、Bevacizumab与化疗的三联组合疗法一线用于晚期非小细胞肺癌患者治疗，在提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150 Phase III）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• NCCN指南推荐在转移性非小细胞患者在铂类化药治疗无效或进展后，特别是对于检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者，可以在二线治疗中使用Atezolizumab（POPLAR Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• 研究表明TMB水平与Atezolizumab临床治疗效果呈正相关（10.1016/j.jtho.2016.11.343）。',
                                  style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab用于不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC Phase III）。\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1高（>=25%）的晚期NSCLC患者，接受Durvalumab治疗比PD-L1低或不表达的患者存在明显的响应率和生存期获益（NCT01693562）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性非小细胞肺癌患者，可明显提升患者的响应率（ATLANTIC Phase II）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 正在开展的三个Durvalumab三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC Phase III， MYSTIC Phase III，NEPTUNE Phase III）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tCheckmate 026 Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。Checkmate 026 Phase III回溯性研究：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中相比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 057 Phase III：转移非鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 017 Phase III：转移鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1200/JCO.2016.34.15_suppl.9017：研究表明接受Nivolumab/pembrolizumab/avelumab治疗的晚期非小细胞肺癌患者，TMB高的群体具有更长的治疗耐受时间（Median time on anti-PD-1/PD-L1 therapy: 64 weeks vs. 17 weeks）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckMate 032 Phase I/II：Nivolumab单药治疗，以及Nivolumab与ipilimumab联合治疗在以前接受过治疗的小细胞肺癌患者中表现出抗肿瘤活性的持久的响应和可控的安全性，TMB高的SCLC患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升（ORR: 46% vs. 16%; 1-year OS: 62% vs. 20%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗将比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 021 Phase II： 帕姆单抗和卡铂、培美曲塞的联合用药在非鳞性晚期NSCLC的一线治疗中是有效且耐受的。三种药物的联合使用将比仅化疗药物使用具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 010 Phase II/ III：在使用铂药基础的化疗治疗后进展的NSCLC患者中，如果存在PD-L1表达（TPS >1%），接受Pembrolizumab治疗（10mg/kg每三周一次）的患者比接受多西他赛治疗的患者在生存期中位数上有110%的延长。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选的晚期NSCLC患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（ORR 18%-22%，26%-31% TC3 IC3）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tImpower 150 Phase III：根据临床试验结果，Atezolizumab、Bevacizumab与化疗，三联组合疗法一线用于晚期肺癌患者，与Bevacizumab和化疗相比，有效率更高（64% VS 48%），可降低38%的疾病进展和死亡风险（PFS 8.3 vs. 6.4），有望提高患者生存期。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPOPLAR Phase II：在使用铂药基础的化疗治疗后进展的NSCLC患者中，接受Atezolizumab治疗的患者比接受多西他赛治疗的患者在总体生存期上有30%的延长；根据2018第二版NCCN NSCLC专家指南，使用Nivolumab和Atezolizumab无需进行PD-L1免疫组化检测，但根据POPLAR II期临床试验的结果，检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者（TC3 or IC3）总体的生存期或更高。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1016/j.jtho.2016.11.343：研究表明不论PD-L1表达筛选与否，晚期NSCLC患者中TMB较高的群体，在Atezolizumab用药有效率上有明显提升（ORR：28% vs. 13%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPACIFIC Phase III：在连续使用铂药基础的放化疗治疗2个以上周期的未进展NSCLC患者，接受Durvalumab治疗的患者比安慰剂组患者能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNCT01693562 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tATLANTIC Phase II：根据临床试验结果，采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性NSCLC患者，与PD-L1阴性患者相比，明显提升了患者的响应率（ORR: 16.4% vs. 7.5%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在评估PD-L1-high和PD-L1-low分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，与Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                       'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                       'medicine_note': medicine_note}
            # 2
        if realMSI == 'MSI-S'and mmr_mean =='正常' and tmb_mean =='高' and tnb_mean =='高':
            Nivolumab_mean = RichText(
                '• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（Checkmate 026）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 最新临床试验后的探索性研究数据显示，TMB高的晚期非小细胞肺癌患者接受Nivolumab治疗比化疗可获得更长的无进展生存期（Checkmate 026）。根据Nature两篇文献的回溯性研究报道，新抗原“fitness”模型中high-fitness患者群体更容易从免疫检查点抑制剂治疗中获益（10.1038/nature24462，10.1038/nature24473）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（Checkmate 057，Checkmate 017）。\n',
                               style="HLAMeanStyle")
            Nivolumab_mean.add(
                '• 研究表明TMB高的患者与接受Nivolumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。\n',
                style="HLAMeanStyle")
            Nivolumab_mean.add('• 临床试验CheckMate 032结果表明，TMB高的小细胞肺癌患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升。与临床试验Checkmate 026非小细胞肺癌研究的横向对比发现，虽然两者亚型不同，但在TMB高、中、低的划分指标上却相当。这两个临床试验相互印证了TMB高的群体更容易从Nivolumab治疗中获益（Checkmate 032）。',
                               style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（>=50%），可以考虑在一线治疗中使用Pembrolizumab（Keynote 024）。\n',
                                          style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与pemetrexed和carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（Keynote 021）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于PD-L1表达（TPS>=1%）的晚期非小细胞肺癌，在铂类药物化疗进展的二线治疗中（Keynote 010）。\n',
                                   style="HLAMeanStyle")
            Pembrolizumab_mean.add('• 研究表明TMB高的患者与接受Pembrolizumab治疗的较长耐受期呈正相关（10.1200/JCO.2016.34.15_suppl.9017）。根据Nature两篇文献的回溯性研究报道，新抗原“fitness”模型中high-fitness患者群体更容易从免疫检查点抑制剂治疗中获益（10.1038/nature24462，10.1038/nature24473）。',
                                   style="HLAMeanStyle")
            Atezolizumab_mean = RichText(
                '• 临床试验表明Atezolizumab在经过PD-L1表达筛选的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（BIRCH Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• 临床试验表明与单独Bevacizumab与化疗相比，Atezolizumab、Bevacizumab与化疗的三联组合疗法一线用于晚期非小细胞肺癌患者治疗，在提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150 Phase III）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add(
                '• NCCN指南推荐在转移性非小细胞患者在铂类化药治疗无效或进展后，特别是对于检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者，可以在二线治疗中使用Atezolizumab（POPLAR Phase II）。\n',
                style="HLAMeanStyle")
            Atezolizumab_mean.add('• 研究表明TMB水平与Atezolizumab临床治疗效果呈正相关（10.1016/j.jtho.2016.11.343）。',
                                  style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab用于不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC Phase III）。\n',
                                       style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明PD-L1高（>=25%）的晚期NSCLC患者，接受Durvalumab治疗比PD-L1低或不表达的患者存在明显的响应率和生存期获益（NCT01693562）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 临床试验表明采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性非小细胞肺癌患者，可明显提升患者的响应率（ATLANTIC Phase II）。\n',
                style="HLAMeanStyle")
            Durvalumab_mean.add(
                '• 正在开展的三个Durvalumab三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC Phase III， MYSTIC Phase III，NEPTUNE Phase III）。',
                style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tCheckmate 026 Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。Checkmate 026 Phase III回溯性研究：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中相比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1038/nature24462：新抗原质量预测模型（fitness model）显示，新抗原质量而非新抗原数量可以作为胰腺导管腺癌预后的分子标记，新抗原质量高的患者群体具有较好的预后生存状况。新抗原质量预测模型与传统的新抗原数量预测模型的区别在于，在传统数量预测的基础上，加入了新抗原展示区分度和致病有效性的权重评分。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1038/nature24473：回溯性研究表明（其中包括在肺癌中的anti-PD-1治疗）新抗原质量预测模型（fitness model）可以预测免疫检查点抑制剂的治疗响应。高-fitness与低-finess相比，具有较好的治疗预后。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 057 Phase III：转移非鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 017 Phase III：转移鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1200/JCO.2016.34.15_suppl.9017：研究表明接受Nivolumab/pembrolizumab/avelumab治疗的晚期非小细胞肺癌患者，TMB高的群体具有更长的治疗耐受时间（Median time on anti-PD-1/PD-L1 therapy: 64周 vs. 17周）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckMate 032 Phase I/II：Nivolumab单药治疗，以及Nivolumab与ipilimumab联合治疗在以前接受过治疗的小细胞肺癌患者中表现出抗肿瘤活性的持久的响应和可控的安全性，TMB高的SCLC患者不论在接受Nivolumab和ipilimumab联合治疗，还是Nivolumab单药治疗中，客观响应率和1年期生存率都有明显提升（ORR: 46% vs. 16%; 1-year OS: 62% vs. 20%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗将比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 021 Phase II： 帕姆单抗和卡铂、培美曲塞的联合用药在非鳞性晚期NSCLC的一线治疗中是有效且耐受的。三种药物的联合使用将比仅化疗药物使用具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 010 Phase II/ III：在使用铂药基础的化疗治疗后进展的NSCLC患者中，如果存在PD-L1表达（TPS >1%），接受Pembrolizumab治疗（10mg/kg每三周一次）的患者比接受多西他赛治疗的患者在生存期中位数上有110%的延长。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选的晚期NSCLC患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（ORR 18%-22%，26%-31% TC3 IC3）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tImpower 150 Phase III：根据临床试验结果，Atezolizumab、Bevacizumab与化疗，三联组合疗法一线用于晚期肺癌患者，与Bevacizumab和化疗相比，有效率更高（64% VS 48%），可降低38%的疾病进展和死亡风险（PFS 8.3 vs. 6.4），有望提高患者生存期。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPOPLAR Phase II：在使用铂药基础的化疗治疗后进展的NSCLC患者中，接受Atezolizumab治疗的患者比接受多西他赛治疗的患者在总体生存期上有30%的延长；根据2018第二版NCCN NSCLC专家指南，使用Nivolumab和Atezolizumab无需进行PD-L1免疫组化检测，但根据POPLAR II期临床试验的结果，检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者（TC3 or IC3）总体的生存期或更高。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1016/j.jtho.2016.11.343：研究表明不论PD-L1表达筛选与否，晚期NSCLC患者中TMB较高的群体，在Atezolizumab用药有效率上有明显提升（ORR：28% vs. 13%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPACIFIC Phase III：在连续使用铂药基础的放化疗治疗2个以上周期的未进展NSCLC患者，接受Durvalumab治疗的患者比安慰剂组患者能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNCT01693562 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tATLANTIC Phase II：根据临床试验结果，采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性NSCLC患者，与PD-L1阴性患者相比，明显提升了患者的响应率（ORR: 16.4% vs. 7.5%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在评估PD-L1-high和PD-L1-low分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，与Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                   'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                   'medicine_note': medicine_note}
        #     4
        if realMSI == 'MSI-S' and mmr_mean == '正常' and (tmb_mean == '低' or tmb_mean == '中') and tnb_mean == '高':
            Nivolumab_mean = RichText('• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（Checkmate 026）。\n', style="HLAMeanStyle")
            Nivolumab_mean.add('• 最新临床试验后的探索性研究数据显示，TMB低的晚期非小细胞肺癌患者接受Nivolumab治疗的中位无进展生存期比化疗更短（Checkmate 026）。根据Nature两篇文献的回溯性研究报道，新抗原“fitness”模型中high-fitness患者群体更容易从免疫检查点抑制剂治疗中获益（10.1038/nature24462，10.1038/nature24473）。\n',style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（Checkmate 057，Checkmate 017）。',style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（>=50%），可以考虑在一线治疗中使用Pembrolizumab（Keynote 024）。\n',style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与pemetrexed和carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（Keynote 021）。\n',style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于PD-L1表达（TPS>=1%）的晚期非小细胞肺癌，在铂类药物化疗进展的二线治疗中（Keynote 010）。',style="HLAMeanStyle")
            Atezolizumab_mean = RichText('• 临床试验表明Atezolizumab在经过PD-L1表达筛选的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（BIRCH Phase II）。\n',style="HLAMeanStyle")
            Atezolizumab_mean.add('• 临床试验表明与单独Bevacizumab与化疗相比，Atezolizumab、Bevacizumab与化疗的三联组合疗法一线用于晚期非小细胞肺癌患者治疗，在提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150 Phase III）。\n',style="HLAMeanStyle")
            Atezolizumab_mean.add('• NCCN指南推荐在转移性非小细胞患者在铂类化药治疗无效或进展后，特别是对于检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者，可以在二线治疗中使用Atezolizumab（POPLAR Phase II）。\n',style="HLAMeanStyle")
            Atezolizumab_mean.add('• 研究表明TMB水平与Atezolizumab临床治疗效果呈正相关（10.1016/j.jtho.2016.11.343）。',style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab用于不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC Phase III）。\n',style="HLAMeanStyle")
            Durvalumab_mean.add('• 临床试验表明PD-L1高（>=25%）的晚期NSCLC患者，接受Durvalumab治疗比PD-L1低或不表达的患者存在明显的响应率和生存期获益（NCT01693562）。\n',style="HLAMeanStyle")
            Durvalumab_mean.add('• 临床试验表明采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性非小细胞肺癌患者，可明显提升患者的响应率（ATLANTIC Phase II）。\n',style="HLAMeanStyle")
            Durvalumab_mean.add('• 正在开展的三个Durvalumab三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC Phase III， MYSTIC Phase III，NEPTUNE Phase III）。',style="HLAMeanStyle")
            medicine_note = RichText(
                '•\tCheckmate 026 Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。Checkmate 026 Phase III回溯性研究：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中相比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1038/nature24462：新抗原质量预测模型（fitness model）显示，新抗原质量而非新抗原数量可以作为胰腺导管腺癌预后的分子标记，新抗原质量高的患者群体具有较好的预后生存状况。新抗原质量预测模型与传统的新抗原数量预测模型的区别在于，在传统数量预测的基础上，加入了新抗原展示区分度和致病有效性的权重评分。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1038/nature24473：回溯性研究表明（其中包括在肺癌中的anti-PD-1治疗）新抗原质量预测模型（fitness model）可以预测免疫检查点抑制剂的治疗响应。高-fitness与低-finess相比，具有较好的治疗预后。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 057 Phase III：转移非鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tCheckmate 017 Phase III：转移鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗将比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 021 Phase II： 帕姆单抗和卡铂、培美曲塞的联合用药在非鳞性晚期NSCLC的一线治疗中是有效且耐受的。三种药物的联合使用将比仅化疗药物使用具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tKeynote 010 Phase II/ III：在使用铂药基础的化疗治疗后进展的NSCLC患者中，如果存在PD-L1表达（TPS >1%），接受Pembrolizumab治疗（10mg/kg每三周一次）的患者比接受多西他赛治疗的患者在生存期中位数上有110%的延长。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选的晚期NSCLC患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（ORR 18%-22%，26%-31% TC3 IC3）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tImpower 150 Phase III：根据临床试验结果，Atezolizumab、Bevacizumab与化疗，三联组合疗法一线用于晚期肺癌患者，与Bevacizumab和化疗相比，有效率更高（64% VS 48%），可降低38%的疾病进展和死亡风险（PFS 8.3 vs. 6.4），有望提高患者生存期。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPOPLAR Phase II：在使用铂药基础的化疗治疗后进展的NSCLC患者中，接受Atezolizumab治疗的患者比接受多西他赛治疗的患者在总体生存期上有30%的延长；根据2018第二版NCCN NSCLC专家指南，使用Nivolumab和Atezolizumab无需进行PD-L1免疫组化检测，但根据POPLAR II期临床试验的结果，检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者（TC3 or IC3）总体的生存期或更高。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\t10.1016/j.jtho.2016.11.343：研究表明不论PD-L1表达筛选与否，晚期NSCLC患者中TMB较高的群体，在Atezolizumab用药有效率上有明显提升（ORR：28% vs. 13%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tPACIFIC Phase III：在连续使用铂药基础的放化疗治疗2个以上周期的未进展NSCLC患者，接受Durvalumab治疗的患者比安慰剂组患者能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNCT01693562 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tATLANTIC Phase II：根据临床试验结果，采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性NSCLC患者，与PD-L1阴性患者相比，明显提升了患者的响应率（ORR: 16.4% vs. 7.5%）。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在评估PD-L1-high和PD-L1-low分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，与Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。\n',
                style="HLAMeanStyle")
            medicine_note.add(
                '•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。',
                style="HLAMeanStyle")
            context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
                   'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
                   'medicine_note': medicine_note}
        #     5
        if realMSI == 'MSI-S' and mmr_mean == '正常' and (tmb_mean == '低' or tmb_mean =='中') and tnb_mean == '低':
            Nivolumab_mean = RichText('• 临床试验表明PD-L1表达（TPS>=5%）的非小细胞肺癌晚期患者接受Nivolumab治疗，并未获得比化疗更长的无进展生存期和整体生存期（Checkmate 026）。\n',style = "HLAMeanStyle")
            Nivolumab_mean.add('• 最新临床试验后的探索性研究数据显示，TMB低的晚期非小细胞肺癌患者接受Nivolumab治疗的中位无进展生存期比化疗更短（Checkmate 026）。\n',style="HLAMeanStyle")
            Nivolumab_mean.add('• FDA批准转移性非小细胞患者在铂类化药治疗无效或进展后，在二线治疗中使用Nivolumab（Checkmate 057，Checkmate 017）。',style="HLAMeanStyle")
            Pembrolizumab_mean = RichText('• 如果PD-L1免疫组化检测呈阳性（>=50%），可以考虑在一线治疗中使用Pembrolizumab（Keynote 024）。\n',style = "HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab与pemetrexed和carboplatin三药联合用于晚期非小细胞肺癌的一线治疗（Keynote 021）。\n',style="HLAMeanStyle")
            Pembrolizumab_mean.add('• FDA批准Pembrolizumab单药可用于PD-L1表达（TPS>=1%）的晚期非小细胞肺癌，在铂类药物化疗进展的二线治疗中（Keynote 010）。',style="HLAMeanStyle")
            Atezolizumab_mean =RichText('• 临床试验表明Atezolizumab在经过PD-L1表达筛选的晚期非小细胞肺癌患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（BIRCH Phase II）。\n',style ="HLAMeanStyle")
            Atezolizumab_mean.add('• 临床试验表明与单独Bevacizumab与化疗相比，Atezolizumab、Bevacizumab与化疗的三联组合疗法一线用于晚期非小细胞肺癌患者治疗，在提高有效率的同时，明显降低了疾病进展和死亡的风险（Impower 150 Phase III）。\n',style="HLAMeanStyle")
            Atezolizumab_mean.add('• NCCN指南推荐在转移性非小细胞患者在铂类化药治疗无效或进展后，特别是对于检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者，可以在二线治疗中使用Atezolizumab（POPLAR Phase II）。\n',style="HLAMeanStyle")
            Atezolizumab_mean.add('• 研究表明TMB水平与Atezolizumab临床治疗效果呈正相关（10.1016/j.jtho.2016.11.343）。',style="HLAMeanStyle")
            Durvalumab_mean = RichText('• NCCN指南推荐Durvalumab用于不可切除的非小细胞肺癌III期患者在同步放化疗后使用的辅助治疗药物（PACIFIC Phase III）。\n',style = "HLAMeanStyle")
            Durvalumab_mean.add('• 临床试验表明PD-L1高（>=25%）的晚期NSCLC患者，接受Durvalumab治疗比PD-L1低或不表达的患者存在明显的响应率和生存期获益（NCT01693562）。\n',style="HLAMeanStyle")
            Durvalumab_mean.add('• 临床试验表明采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性非小细胞肺癌患者，可明显提升患者的响应率（ATLANTIC Phase II）。\n',style="HLAMeanStyle")
            Durvalumab_mean.add('• 正在开展的三个Durvalumab三期临床试验包括：ARTIC，MYSTIC，NEPTUNE（ARTIC Phase III， MYSTIC Phase III，NEPTUNE Phase III）。',style="HLAMeanStyle")
            medicine_note = RichText('•\tCheckmate 026 Phase III：PD-L1表达（TPS>=5%）的晚期NSCLC患者，接受Nivolumab治疗与化疗相比，并未取得预期的临床获益（Median PFS: 4.2 vs. 5.9; Median OS: 14.4 vs. 13.2 ）。Checkmate 026 Phase III回溯性研究：TMB高的NSCLC患者群体可在Nivolumab治疗中获益（Median PFS: 9.7 vs. 5.8），TMB低的NSCLC群体在Nivolumab治疗中相比化疗具有更短的无进展生存期（Median PFS: 4.1 vs. 6.9）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tCheckmate 057 Phase III：转移非鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：29% vs. 16% ）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tCheckmate 017 Phase III：转移鳞性NSCLC患者接受Nivolumab单药治疗将比接受docetaxel治疗的总体生存期更长（24-month OS：23% vs. 8%）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tKeynote 024 Phase III：PD-L1表达(TPS>=50%)的晚期NSCLC患者接受Pembrolizumab治疗将比接受platinum化疗具有显著延长的无进展生存期和整体生存期（Median PFS: 10.3 vs. 6.0; 6-month OS: 80.2% vs. 72.4%）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tKeynote 021 Phase II： 帕姆单抗和卡铂、培美曲塞的联合用药在非鳞性晚期NSCLC的一线治疗中是有效且耐受的。三种药物的联合使用将比仅化疗药物使用具有更高的整体响应率和更长的中位无进展生存期（ORR: 55% vs. 29%; Median PFS: 13.0 vs. 8.9）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tKeynote 010 Phase II/ III：在使用铂药基础的化疗治疗后进展的NSCLC患者中，如果存在PD-L1表达（TPS >1%），接受Pembrolizumab治疗（10mg/kg每三周一次）的患者比接受多西他赛治疗的患者在生存期中位数上有110%的延长。\n',style="HLAMeanStyle")
            medicine_note.add('•\tBIRCH Phase II：Atezolizumab在经过PD-L1表达筛选的晚期NSCLC患者中，表现良好的耐受性和响应率，提示PD-L1表达状态作为Atezolizumab用药获益的分子标记的可能性（ORR 18%-22%，26%-31% TC3 IC3）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tImpower 150 Phase III：根据临床试验结果，Atezolizumab、Bevacizumab与化疗，三联组合疗法一线用于晚期肺癌患者，与Bevacizumab和化疗相比，有效率更高（64% VS 48%），可降低38%的疾病进展和死亡风险（PFS 8.3 vs. 6.4），有望提高患者生存期。\n',style="HLAMeanStyle")
            medicine_note.add('•\tPOPLAR Phase II：在使用铂药基础的化疗治疗后进展的NSCLC患者中，接受Atezolizumab治疗的患者比接受多西他赛治疗的患者在总体生存期上有30%的延长；根据2018第二版NCCN NSCLC专家指南，使用Nivolumab和Atezolizumab无需进行PD-L1免疫组化检测，但根据POPLAR II期临床试验的结果，检测到PD-L1表达和肿瘤浸润淋巴细胞（TIL）的患者（TC3 or IC3）总体的生存期或更高。\n',style="HLAMeanStyle")
            medicine_note.add('•\t10.1016/j.jtho.2016.11.343：研究表明不论PD-L1表达筛选与否，晚期NSCLC患者中TMB较高的群体，在Atezolizumab用药有效率上有明显提升（ORR：28% vs. 13%）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tPACIFIC Phase III：在连续使用铂药基础的放化疗治疗2个以上周期的未进展NSCLC患者，接受Durvalumab治疗的患者比安慰剂组患者能够获得更高的无进展生存期和生存时间（Median PFS: 16.8 vs. 5.6; Median time to death: 23.2 vs. 14.6）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tNCT01693562 Phase I/II：在晚期NSCLC患者中，PD-L1高表达（TPS >=25%）的患者接受Durvalumab治疗比PD-L1低表达的患者获得更高的响应率和更长的生存期（ORR: 25% vs. 6%; Median OS: 15.4 vs. 7.6）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tATLANTIC Phase II：根据临床试验结果，采用Durvalumab治疗已经接受过二线以上系统性治疗后失败的PD-L1阳性的局部晚期或转移性NSCLC患者，与PD-L1阴性患者相比，明显提升了患者的响应率（ORR: 16.4% vs. 7.5%）。\n',style="HLAMeanStyle")
            medicine_note.add('•\tARTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在评估PD-L1-high和PD-L1-low分组中Durvalumab和Soc疗效对比，以及Durvalumab和Tremelimumab药物联用和单药疗效对比的临床III期试验，目前正在开展中。\n',style="HLAMeanStyle")
            medicine_note.add('•\tMYSTIC Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者的，旨在PD-L1阳性和阴性分组中，评估Durvalumab和Tremelimumab药物联用，与Durvalumab单用，以及Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。\n',style="HLAMeanStyle")
            medicine_note.add('•\tNEPTUNE Phase III：该临床试验是一项针对局部晚期或转移性NSCLC患者（不论PD-L1表达与否）的，旨在评估Durvalumab和Tremelimumab药物联用，与Soc、铂类化疗疗效对比的临床III期试验，目前正在开展中。',style="HLAMeanStyle")

            context = {'Nivolumab_mean':Nivolumab_mean,'Pembrolizumab_mean':Pembrolizumab_mean,'Atezolizumab_mean':Atezolizumab_mean,'Durvalumab_mean':Durvalumab_mean,'medicine_note':medicine_note}

        # else:
        #     Nivolumab_mean = RichText('未知',style="HLAMeanStyle")
        #     Pembrolizumab_mean = RichText('未知',style="HLAMeanStyle")
        #     Atezolizumab_mean = RichText('未知',style = "HLAMeanStyle")
        #     Durvalumab_mean = RichText('未知',style="HLAMeanStyle")
        #     medicine_note = RichText('未知',style="HLAMeanStyle")
        #     context = {'Nivolumab_mean': Nivolumab_mean, 'Pembrolizumab_mean': Pembrolizumab_mean,
        #                'Atezolizumab_mean': Atezolizumab_mean, 'Durvalumab_mean': Durvalumab_mean,
        #                'medicine_note': medicine_note}
        print (context)
        #     6

    def run(self):
        content ={}
        global context
        BasicInfoName = self.kwargs.get('Basic_InfoName')
        MSIPathName = self.kwargs.get('MSI_PathName')
        ResultFileName = self.kwargs.get('Result_FileName')
        print (ResultFileName)
        ResultFileInst = FileIter(ResultFileName)
        for ResultItem in ResultFileInst:
            print (ResultItem)
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
        doc.render(content)
        doc.save("/disk/lulu/autoreport/output/generated_doc.docx")  # 保存

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
                context['Neo_contents'].append({'cols': [InputItem[0], InputItem[1], InputItem[2], InputItem[3], InputItem[4]]})
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
        options, args = getopt.getopt(argv, "hB:M:R:",["help", "Basic_Info=", "MSI_Path=", "Result_File="])
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
        ''')


def cmdDict():
    global Basic_Info
    global MSI_Path
    global Result_File
    callerDict = {
        'Basic_InfoName': Basic_Info,
        'MSI_PathName': MSI_Path,
        'Result_FileName': Result_File,
    }
    return callerDict


if __name__ == '__main__':
    Basic_Info = "" #患者基本信息以及MSI图路径的配置文件（csv配置文件）
    MSI_Path = "" #MSI图的路径
    Result_File = "" #流程给出的结果路径文件
    if len(sys.argv) < 2:
        print ('please input parameters! or You can input "--help" to get the usage')
        sys.exit()
    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        print (callerDict)
        # print callerDict
        inst = allCallerSimple(**callerDict)
        inst.run()

