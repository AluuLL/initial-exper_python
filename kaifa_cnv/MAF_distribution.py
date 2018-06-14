with open(
        "/disk/lulu/Hiseq30x-1_rawbam_0.5.sort.merge_deletion_1K+_pickedsnp.MAF_chunhe.gvc_pickbenchmark.txt") as file:
    # f = open("out.txt", "w")
    global listprint
    listprint = []
    count = 0
    num = 0
    flag = 0
    for line in file:
        list = line.strip().split("\t")
        if listprint:
            if flag == 0:
                MAF_value = 0
                num = num + 1
                MAF_value += float(listprint[11])
                if float(listprint[11]) >= 0.8:
                    count = count + 1
                if list[1] == listprint[1] and list[2] == listprint[2] and list[3] == listprint[3]:
                    flag = 1
                    num = num + 1
                    MAF_value += float(list[11])
                    if float(list[11]) >= 0.8:
                        count = count + 1
                        listprint = list
                        # if
                else:
                    flag = 0
                    ratio = count / num
                    print("\t".join(listprint).rstrip() + "\t" + str(MAF_value / num) + "\t" + str(num) + "\t" + str(
                        count) + "\t" + str(ratio)),
                    # print ("\t"+str(MAF_value/num))
                    # print (listprint)
                    listprint = list
                    count = 0
                    num = 0


            else:
                if list[1] == listprint[1] and list[2] == listprint[2] and list[3] == listprint[3]:
                    flag = 1
                    num = num + 1
                    MAF_value += float(list[11])
                    if float(list[11]) >= 0.8:
                        count = count + 1
                        listprint = list

                else:
                    flag = 0
                    ratio = count / num
                    print("\t".join(listprint).rstrip() + "\t" + str(MAF_value / num) + "\t" + str(num) + "\t" + str(
                        count) + "\t" + str(ratio)),
                    # print ("\t"+str(MAF_value/num))
                    # print(listprint)
                    listprint = list
                    count = 0
                    num = 0


        else:
            listprint = list
