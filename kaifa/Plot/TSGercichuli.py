file = open("/disk/lulu/database/TSGene/pro/TSG.final.1.txt")
import re
for line in file:
    line1 = line.split("\t")
    for id, value in enumerate(line1):
        #   b = re.sub("^\D", '-', line)
        #  print b,
        # print line.replace(" \n","-\n"),
        b = re.sub(r"_$", "\t", line1[id])
        print b,
