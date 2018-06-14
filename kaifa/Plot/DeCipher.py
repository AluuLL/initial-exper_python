import re
file = open("/disk/lulu/database/DD/pro/DDG2P_22_11_2017_pro.csv")
#line = '5532303..5565780'
#print line.replace("..","\t")

#b = re.sub("\.\." , '\t', line)
#print b
for line in file:
    list = line.strip().split(",")
    ###print list[0]
    line1 =','.join(list[1:])
    #print line1
    list2 =line1.strip().split(",")
    ###print list2[0]
    line11 =','.join(list2[1:])
    #print line11
    list21 =line11.strip().split(",")
    list3 =list21[-11:]
    ##print list3
    list4 =list21[:-11]
    line4 =''.join(list4)
   ### print line4
   ## print list4
    line2 =','.join(list3)
    #print line2
    line3 =re.sub(",",'\t',line2)
    #print line3
    ####print list[0]+"\t"+list2[0]+"\t"+line4+"\t"+line3
    line5 = list[0]+"\t"+list2[0]+"\t"+line4+"\t"+line3
    line6 =re.sub("\"",'',line5)
    print line6
    #list1.insert(0,list[0])
    #print list1
   # line1=re.sub("\"",'',line)
   # line2=re.sub(",",'\t',line1)
   # print line2,

