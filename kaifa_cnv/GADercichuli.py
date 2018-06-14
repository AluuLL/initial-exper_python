file = open("/disk/lulu/database/GAD/data/GADCDC/pro/24.txt")
import re
for line in file:
    line1 = line.split("\t")
    for id, value in enumerate(line1):
        #   b = re.sub("^\D", '-', line)
        #  print b,
        # print line.replace(" \n","-\n"),
        b = re.sub(r"_$", "", line1[id])
        print b,
