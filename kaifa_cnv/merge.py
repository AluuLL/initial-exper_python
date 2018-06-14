with open("/disk/lulu/Hiseq_30X_50bp-3.germ.0.5.sort.CBS") as file:
#f = open("out.txt", "w")
    global listprint
    listprint=[]
    for line in file:
        list = line.strip().split("\t")
        for i,j in enumerate(list):
            if listprint:
                # print (list[1],listprint[1],list[10],listprint[10])
                if list[1]==listprint[1] and list[10]==listprint[10]:
                    listprint[3]=list[3]
                    if list[4]!="NA":
                        listprint[4] = str(float((float(list[4]) + float(listprint[4]))/2))
                    # listprint[4]=str(int((int(list[4])+int(listprint[4]))/2))
                    if list[5]!="NA":
                        listprint[5]=str((float(list[5])+float(list[5]))/2)
                    if list[6] != "NA":
                        listprint[6]=str((float(list[6])+float(list[6]))/2)
                    if list[7] != "NA":
                        listprint[7]=str((float(list[7])+float(list[7]))/2)
                    if list[8] != "NA":
                        listprint[8]=str((float(list[8])+float(list[8]))/2)
                    if list[9] != "NA":
                        listprint[9]=str((float(list[9])+float(list[9]))/2)
                else:
                    print ("\t".join(listprint))
                    listprint=list
            else:
                listprint=list
