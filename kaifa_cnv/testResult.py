import re
from docxtpl import DocxTemplate, RichText
from docx.shared import Pt

####test Result including checkpoint and HLA
def checkPoint(TMBFileName, NeoStatisFileName, MMRFileName, POLFileName):

    with open(TMBFileName,'r',encoding='utf-8') as snv:
        line = snv.readlines()[1]
        line = line.strip('\n').split('\t')
        nonsys_num = int(line[1])
        sys_num = int(line[2])
        if line[3] == '-':
            kaks = 'N/A'
        else:
            kaks = round(float(line[3]), 2)
        tmb_result = round(float(line[6]),2)
    with open(NeoStatisFileName,'r',encoding='utf-8') as neo:
        line = neo.readline()
        line = line.strip('\n').split('\t')
        neo_num = int(line[1])
    with open(MMRFileName,'r',encoding='utf-8') as mmr:
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
    if tmb_result >= 9 :
        tmb_mean = '高'
    elif tmb_result < 3:
        tmb_mean = '低'
    else:
        tmb_mean = '中'
    #
    if nonsys_num >= 248:
        nonsys_mean = '高'
        tmb_des = "本检测得到的TMB结果高于平均值"
        tmb_status = "TMB_H(>248个非同义突变位点)"
    elif nonsys_num < 143:
        nonsys_mean = '低'
        tmb_des = "本检测得到的TMB结果低于平均值"
        tmb_status = "TMB_L(0-143个非同义突变位点)"
    else:
        nonsys_mean = '中'
        tmb_des = "本检测得到的TMB结果位于中位数附近"
        tmb_status = "TMB_M(143-248个非同义突变位点)"
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
        kaks_des = ''
    elif kaks >= 3:
        kaks_mean = '较高'
        kaks_des = '＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio大于3.0，反映样本中的肿瘤细胞的增殖能力处于较高状态；'
    elif kaks < 2.5:
        kaks_mean = '较低'
        kaks_des='＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio小于2.5，反映样本中的肿瘤细胞的增殖能力处于较低状态；'
    else:
        kaks_mean = '中性'
        kaks_des='＊非同义突变／同义突变比值（A/S ratio）是一种衡量肿瘤进化保守性的指标，这一指标越大代表肿瘤的增殖能力越高，本次检测从样本中测量到的A/S ratio大于2.5小于3.0，反映样本中的肿瘤细胞的增殖能力处于中性状态；'
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
        'tmb_result': str(tmb_result)+'/Mb',
        'tmb_mean':tmb_mean,
        'nonsys_num':str(nonsys_num)+'个',
        'nonsys_mean':nonsys_mean,
        'sys_num':str(sys_num)+'个',
        'sys_mean':sys_mean,
        'kaks_value':kaks,
        'kaks_mean':kaks_mean,
        'mmr_result':mmr_result,
        'mmr_mean':mmr_mean,
        'pol_result':pol_result,
        'pol_mean':pol_mean,
        'neo_num':str(neo_num)+'个',
        'tmb_des':tmb_des,
        'tmb_status':tmb_status

    }
    #print (content)
    return content
def separateHLA(HLA):
    HLA_A = []
    HLA_B = []
    HLA_C = []
    for item in HLA:
        item = item[4:] ###delete HLA-
        if re.match('^A', item) is not None:
            HLA_A.append(item)
        if re.match('^B', item) is not None:
            HLA_B.append(item)
        if re.match('^C', item) is not None:
            HLA_C.append(item)
    content ={
        'cols':['\n'.join(HLA_A),'\n'.join(HLA_B),'\n'.join(HLA_C)],
        'value':{'A':HLA_A,'B':HLA_B,'C':HLA_C}
    }
    return content
def getHeterozy(HLA):
    if len(HLA) == 1:
        return 'isozy' ##纯合
    elif len(HLA) == 0:
        return 'NA'  #无
    else:
        return 'heterozy'  #杂合
def getMean(normal,tumor):
    mean = RichText('注：人群的HLA-I分型存在广泛的多态性，本报告所列举的HLA-I分型结果由基因测序获得')
    B62 = ['B*15:02', 'B*15:12', 'B*15:13', 'B*46:01', 'B*52:01']
    B44 = ['B*18:01', 'B*37:01', 'B*40:01', 'B*40:02', 'B*40:06', 'B*44:02', 'B*44:03', 'B*45:01']
    PD1 = ['B*15:01'] + B62 + B44
    ####
    if getHeterozy(normal['A']) =='heterozy' and getHeterozy(normal['B']) =='heterozy' and getHeterozy(normal['C']) =='heterozy':
        mean.add('\n＊本次检测从正常体细胞检测到所有的等位基因都处于杂合状态，最新研究显示相较于至少一个位置的等位基因为纯合状态的患者，全部为杂合状态的患者在接受anti-PD-1药物治疗时生存期中位数更长（Chowell ')
        mean.add('et al., Science）',italic=True)
        if getHeterozy(tumor['A']) =='heterozy' and getHeterozy(tumor['B'])=='heterozy' and getHeterozy(tumor['C'])=='heterozy' :
            mean.add('\n＊40%的非小细胞肺癌患者的肿瘤样本中检测到HLA-I的杂合性缺失，这与亚克隆的新抗原负载高相关（McGranahan ')
            mean.add('et al., Cell',italic=True)
            mean.add('），而本次检测未发现肿瘤样本和正常体细胞中存在HLA-I的分型差异')
    if getHeterozy(normal['A']) =='isozy' or getHeterozy(normal['B'])=='isozy' or getHeterozy(normal['C'])=='isozy' :
        mean.add('\n＊本次检测从正常细胞中检测到存在至少一个等位基因为纯合状态，根据最新研究显示相较于所有等位基因都处于杂合状态的患者，至少一个等位基因为纯合状态的患者在接受anti-PD-1药物治疗时生存期中位数较短（Chowell ')
        mean.add('et al., Science）',italic=True)
    ###
    if len(set(normal['B']) & set(B62))>0 and len(set(tumor['B']) & set(B62))>0:
        mean.add('\n＊最新研究显示携带有HLA-B62 supertype的等位基因的患者接受anti-PD-1治疗的预后较差（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从正常细胞和肿瘤组织中都检测到HLA-B62 supertype中的等位基因')
    elif len(set(normal['B']) & set(B62))==0 and len(set(tumor['B']) & set(B62))>0:
        mean.add('\n＊最新研究显示携带有HLA-B62 supertype的等位基因的患者接受anti-PD-1治疗的预后较差（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从肿瘤组织中检测到HLA-B62 supertype中的等位基因')
    elif len(set(normal['B']) & set(B62))>0 and len(set(tumor['B']) & set(B62))==0:
        mean.add('\n＊最新研究显示携带有HLA-B62 supertype的等位基因的患者接受anti-PD-1治疗的预后较差（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从正常细胞中检测到HLA-B62 supertype中的等位基因')
    ###
    if 'B*15:01' in normal['B'] and 'B*15:01' in tumor['B']:
        mean.add('\n＊最新研究显示携带有HLA-B62 supertype的B*15:01等位基因的患者接受anti-PD-1治疗的预后较差，这可能是因为B*15:01 的分子结构会影响T细胞对肿瘤细胞的识别能力（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从正常组织和肿瘤组织中都检测到B*15:01')
    elif not 'B*15:01' in normal['B'] and 'B*15:01' in tumor['B']:
        mean.add('\n＊最新研究显示携带有HLA-B62 supertype的B*15:01等位基因的患者接受anti-PD-1治疗的预后较差，这可能是因为B*15:01 的分子结构会影响T细胞对肿瘤细胞的识别能力（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从肿瘤组织中检测到B*15:01')
    elif 'B*15:01' in normal['B'] and not 'B*15:01' in tumor['B']:
        mean.add('\n＊最新研究显示携带有HLA-B62 supertype的B*15:01等位基因的患者接受anti-PD-1治疗的预后较差，这可能是因为B*15:01 的分子结构会影响T细胞对肿瘤细胞的识别能力（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从正常细胞中检测到B*15:01')
    ###
    if len(set(normal['B']) & set(B44))>0 and len(set(tumor['B']) & set(B44))>0:
        mean.add('\n＊最新研究显示携带有HLA-B44 supertype的等位基因的患者接受anti-PD-1治疗的生存期中位数更长（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从正常细胞和肿瘤组织中都检测到HLA-B44 supertype中的等位基因')
    elif len(set(normal['B']) & set(B44))==0 and len(set(tumor['B']) & set(B44))>0:
        mean.add('\n＊最新研究显示携带有HLA-B44 supertype的等位基因的患者接受anti-PD-1治疗的生存期中位数更长（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从肿瘤组织中检测到HLA-B44 supertype中的等位基因')
    elif len(set(normal['B']) & set(B44))>0 and len(set(tumor['B']) & set(B44))>0:
        mean.add('\n＊最新研究显示携带有HLA-B44 supertype的等位基因的患者接受anti-PD-1治疗的生存期中位数更长（Chowell ')
        mean.add('et al., Science',italic=True)
        mean.add('），本次检测从正常细胞中检测到HLA-B44 supertype中的等位基因')
    #####
    if len(set(normal['B']) & set(PD1))==0 and len(set(tumor['B']) & set(PD1))==0:
        mean.add('\n＊本次检测未发现任何已知的影响anti-PD-1治疗预后的HLA等位基因')
    ###
    #mean='\n'.join(mean)
    return mean
def HLA(HLAFileName):
    with open(HLAFileName,'r',encoding='utf-8') as hla:
        line = hla.readlines()
        normal = line[0].strip('\n').split(',')
        tumor = line[1].strip('\n').split(',')
        normal = separateHLA(normal)
        tumor = separateHLA(tumor)

        mean = getMean(normal['value'],tumor['value'])
    content={
        'hla_contents':[
            {'label':'正常细胞中的HLA-I分型：','cols':normal['cols']},
            {'label':'肿瘤组织中的HLA-I分型：','cols':tumor['cols']}
        ],
        'hla_mean':mean
    }
    return content
