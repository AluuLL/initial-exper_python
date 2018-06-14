# fo =open("/disk/lulu/TCGA11.txt","w")
with open(r"/disk/lulu/TCGA1.txt","r") as TCGA:
    temp=[]
    cancerlist=[]
    cancer =[]
    for line in TCGA:
        list = line.strip().split("\t")
        temp = list[0]
        cancerlist.append(temp)
    cancer = sorted(set(cancerlist))
    print (cancer)
    TCGAlist=[]
    for item in cancer:
        # print (item)
        dict = {item: []}
        with open(r"/disk/lulu/TCGA1.txt", "r") as TCGA1:
            for line in TCGA1:
                list = line.strip().split("\t")
                if item==list[0]:
                    dict[item].append(list[2])
        TCGAlist.append(dict)
    print (TCGAlist)


    # print (dict)
    #     temp.append(line1)
    # mytemp = sorted(set(temp))
    # for item in mytemp:
    #     fo.write(item+"\t"+str(round(temp.count(item)/38,2))+"\n")
    #     # print(item+"\t"+str(round(temp.count(item)/38,2))+"\n")