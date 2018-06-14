file = open("/disk/lulu/database/cnvd/pro/linsh.pro.txt")
#f = open("out.txt", "w")
for line in file:
 #   print line,
    list = line.strip().split("\t")
   # print list
    if "|" in list[0]:
        list1 = list[0].strip().split("|")
        print list1[0],"\t",list[1],"\t",list[2],"\t",list[3],"\t",list[4],"\t",list[5],"\t",list[6],"\t",list[7]
        print list1[1],"\t",list[1],"\t",list[2],"\t",list[3],"\t",list[4],"\t",list[5],"\t",list[6],"\t",list[7]
    elif ","in list[0]:
        list1 = list[0].strip().split(",")
        print list1[0], "\t", list[1], "\t", list[2], "\t", list[3], "\t", list[4], "\t", list[5], "\t", list[6], "\t", \
        list[7]
        print list1[1], "\t", list[1], "\t", list[2], "\t", list[3], "\t", list[4], "\t", list[5], "\t", list[6], "\t", \
        list[7]

