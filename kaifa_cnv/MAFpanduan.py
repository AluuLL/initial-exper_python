with open("/disk/lulu/Hiseq30x-1_rawbam_0.5.sort.merge_deletion_1K+_pickedsnp.MAF.CBS") as file:
#f = open("out.txt", "w")
    global listprint
    listprint=[]
    count=0
    num=0
    flag=0
    for line in file:
        list = line.strip().split("\t")
        if listprint:
            if flag==0:
                num =num+1
                if float(listprint[11])>=0.8:
                    count=count+1
            # print (list[1],listprint[1],list[10],listprint[10])
                if list[1]==listprint[1] and list[2]==listprint[2] and list[3]==listprint[3]:
                    flag=1
                    num =num+1
                    if float(list[11])>= 0.8 :
                        count=count+1
                        listprint=list
                else:
                    flag=0
                    ratio=count/num
                    if ratio>=0.7:
                        print("\t".join(listprint))
                        # print (listprint)
                        listprint=list
                        count=0
                        num=0
                    else:
                        listprint=list
                        count=0
                        num=0

            else:
                if list[1] == listprint[1] and list[2] == listprint[2] and list[3] == listprint[3]:
                    flag = 1
                    num = num + 1
                    if float(list[11]) >= 0.8:
                        count = count + 1
                        listprint = list
                else:
                    flag = 0

                    ratio = count / num
                    if ratio >= 0.7:
                        print("\t".join(listprint))
                        #print(listprint)
                        listprint = list
                        count = 0
                        num = 0
                    else:
                        listprint=list
                        count=0
                        num=0
        else:
            listprint=list
