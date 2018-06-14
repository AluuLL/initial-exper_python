file = open("/disk/lulu/Hiseq_30X_50bp-3.germ.raw.CBS")
#f = open("out.txt", "w")
for line in file:
 #   print line,
    list = line.strip().split("\t")
    if float(list[5]) <= (-0.5):
        print (list[0]+"\t"+list[1]+"\t"+list[2]+"\t"+list[3]+"\t"+list[4]+"\t"+list[5]+"\t"+list[6]+"\t"+list[7]+"\t"+list[8]+"\t"+list[9]+"\t"+list[10]+"\t"+"loss"),

    elif float(list[5]) >=0.5:
        print (list[0]+"\t"+list[1]+"\t"+list[2]+"\t"+list[3]+"\t"+list[4]+"\t"+list[5]+"\t"+list[6]+"\t"+list[7]+"\t"+list[8]+"\t"+list[9]+"\t"+list[10]+"\t"+"gain"),
    else:
        print (list[0]+"\t"+list[1]+"\t"+list[2]+"\t"+list[3]+"\t"+list[4]+"\t"+list[5]+"\t"+list[6]+"\t"+list[7]+"\t"+list[8]+"\t"+list[9]+"\t"+list[10]+"\t"+"normal"),


   # print list
   #  if list[4] == "-":
   #      line1 = line.strip().replace("-", "")
   #      print (line1)
   #  #        print >> f, "%s" % line1
   #  else:
   #      print (list[0], "\t", list[1], "\t", list[2], "\t", list[3], "\t", list[5], "\t", list[6], "\t", list[7], "\t", list[8])
   #      list1 = list[4].strip().split('|')
   #      for i in list1:
   #          print (list[0], "\t", list[1], "\t", list[2], "\t", i, "\t", list[5], "\t", list[6], "\t", list[7], "\t", list[8])