import re
file = open("/disk/lulu/database/COSMIC/pro/Cosmic_getlie.txt")
#line = '5532303..5565780'
#print line.replace("..","\t")

#b = re.sub("\.\." , '\t', line)
#print b
for line in file:
    line1=re.sub("\.\.",'\t',line)
    print line1,
