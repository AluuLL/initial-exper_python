
####test Result including checkpoint and HLA
def testResult(SNVFileName, NeoFileName, MMRFileName, POLFileName):
    totalNum = 0
    nonsysNum = 0
    sysNum = 0
    with open(SNVFileName,'r',encoding='utf-8') as snv:
        for line in snv:
            line = line.strip('\n').split('\t')
            if line[4] == '同义突变':
                sysNum += 1
            elif line[4] == "非同义突变":
                nonsysNum += 1
            totalNum += 1
    ######################TMB
    tmb_result = round(totalNum/39,2)
    if tmb_result >= 9 :
        tmb_mean = '高'
    elif tmb_result < 3:
        tmb_mean = '低'
    else:
        tmb_mean = '中'
    #
    if nonsysNum >= 248:
        nonsys_mean = '高'
    elif nonsysNum < 143:
        nonsys_mean = '低'
    else:
        nonsys_mean = '中'
    #
    if sysNum >= 100:
        sys_mean = '高'
    elif sysNum < 57:
        sys_mean = '低'
    else:
        sys_mean = '中'
    #
    kaks = round(nonsysNum /  sysNum,2)
    if kaks >= 3:
        kaks_mean = '较高'
    elif kaks < 2.5:
        kaks_mean = '较低'
    else:
        kaks_mean = '中性'
    content = {
        'tmb_result': str(tmb_result)+'/Mb',
        'tmb_mean':tmb_mean,
        'nonsys_num':nonsysNum,
        'nonsys_mean':nonsys_mean,
        'sys_num':sysNum,
        'sys_mean':sys_mean,
        'kaks_value':kaks,
        'kaks_mean':kaks_mean
    }
    print (content)
    return content