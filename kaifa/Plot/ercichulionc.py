file = open("/disk/lulu/database/oncogene/oncogene_Tsg/all.txt")
#f = open("out.txt", "w")
for line in file:
 #   print line,
    list = line.strip().split("\t")
   # print list
    if "TSG" in list[7] :
         list1 = "\t".join(list)+"\n"
         print list1,