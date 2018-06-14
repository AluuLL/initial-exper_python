file = open("/disk/lulu/database/TSGene/pro/TSG.genepos.qukong.txt")
#f = open("out.txt", "w")
for line in file:
 #   print line,
    list = line.strip().split("\t")
   # print list
    if list[4] == "-":
        line1 = line.strip().replace("-", "")
        print (line1)
    #        print >> f, "%s" % line1
    else:
        print (list[0], "\t", list[1], "\t", list[2], "\t", list[3], "\t", list[5], "\t", list[6], "\t", list[7], "\t", list[8])
        list1 = list[4].strip().split('|')
        for i in list1:
            print (list[0], "\t", list[1], "\t", list[2], "\t", i, "\t", list[5], "\t", list[6], "\t", list[7], "\t", list[8])