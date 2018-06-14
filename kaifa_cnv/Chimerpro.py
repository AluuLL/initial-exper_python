import re
file = open("/disk/lulu/database/ChimerDB/ChimerDB3.0_prohead_for.txt")
#line = '5532303..5565780'
#print line.replace("..","\t")

#b = re.sub("\.\." , '\t', line)
#print b
for line in file:
   line1=re.sub("u\'\'",'-',line)
   line2=re.sub("u\'",'',line1)
   line3=re.sub("\'",'',line2)
   line4=re.sub(",",'\t',line3)
   line5=re.sub("[\t\t]+",'\t',line4)
   print line5,
