file = open("/disk/lulu/database/oncogene/oncogene_Tsg/9.txt")
import re
for id,line in enumerate(file):
 #   b = re.sub("^\D", '-', line)
  #  print b,
    #print line.replace(" \n","-\n"),
    if '_' in line:
        print line,
    elif '-' in line:
        print line,
    elif line.strip('\n').isalnum() is False:
        print line.replace("\n","-\n"),
    else:
        print line,
        #print id,line,len(line)
#chulikonghang