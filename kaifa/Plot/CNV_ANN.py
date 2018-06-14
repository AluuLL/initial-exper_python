#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import re
from itertools import *
import time


class FileIter():
    def __init__(self, fileName):
        try:
            self.file = open(fileName, 'r')
        except IOError as E:
            self.ERROR = True
            print "Can't open %s!" % (fileName)
            print E

    def next(self):
        line = self.file.readline()
        if line == '':
            raise StopIteration
        else:
            return line.strip('\n').split('\t')

    def __iter__(self):
        return self


class allCallerSimple():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        #  def outLine(self,inputList,num,mainLines,sampleLines):
        #     outputList = []
        #    for id in range(0,num,1):
        #       outputList.append(map(lambda x :x if  x <= mainLines else x + sampleLines*id,inputList))
        #  return  outputList

    def prodatabase(self, database):
        if database == "1000Genoeme":
            return database.replace("1000Genome", "../database/1000Genome.txt")
        if database == "DGV":
            return database.replace("DGV", "../database/DGV.txt")
        if database == "dbvar":
            return database.replace("dbvar", "../database/dbvar.txt")
        if database == "CNVD":
            return database.replace("CNVD", "../database/cnvd.txt")
        if database == "DD1":
            return database.replace("DD1", "../database/DD1.txt")
        if database == "DD2":
            return database.replace("DD2", "../database/DD2.txt")
        if database == "GAD":
            return database.replace("GAD", "../database/GAD.txt")
        if database == "Cosmic":
            return database.replace("Cosmic", "../database/Cosmic.txt")
        if database == "TSGene":
            return database.replace("TSGene", "../database/TSG.txt")
        if database == "Oncogene":
            return database.replace("Oncogene", "../database/ocg.txt")
        else:
            print "Have errors in database parameter,you can use '--help' to find the right database format"
            sys.exit()

    def addtitle(self, outputfile, headlist, baselist, leninput):
        line0 = []
        GenomeTitle = ["Chr", "Start", "END", "ID", "REF", "ALT", "CS", "IMPRECISE", "SVTYPE", "AC", "AF", "NS", "AN",
                       "EAS_AF", "EUR_AF", "AFR_AF", "AMR_AF", "SAS_AF", "DP"]
        DGVTitle = ["Chr", "Start", "End", "Variantaccession", "Varianttype", "Variantsubtype", "Method",
                    "Supportingvariants", "Samplesize", "Observedgains", "Observedlosses", "Genes"]
        dbvarTitle = ["Chr", "Start", "End", "Mut_type"]
        CNVDTitle = ["Chr", "Start", "End", "Region", "Mut_type", "Gene_name", "Disease_name", "Frenquency"]
        DD1Title = ["Chr", "Start", "End", "Gene_symbol", "Disease_name", "DDD_category", "Allelic_requirement",
                    "Mutation_consequence", "Organ_specificity_list"]
        DD2Title = ["Chr", "Start", "End", "Population_cnv_id", "Deletion_observations", "Deletion_frequency",
                    "Duplication_observations", "Duplication_frequency", "Observations", "Frequency", "Type",
                    "Sample_size", "Study"]
        GADTitle = ["Chr", "Start", "End", "ID", "ALTNAME", "DISEASE", "DIS_CLAS", "CH_BAND", "GENE", "P_VALUE",
                    "ALLEL_AU", "ALLEL_EF", "PLYM_CLS", "POPULATN", "STDYSIZE", "STDYSZB", "STDYSZTT", "Molephen",
                    "Conclusion", "Study_info", "Env_factor", "GI_COMB_ENV", "GI_RELEV2DISEASE", "RSNUM", "MESHDIS"]
        CosmicTitle = ["Chr", "Start", "End", "CNV_ID", "Id_gene", "Gene_name", "Primary_site", "Site_subtype_1",
                       "Site_subtype_2", "Site_subtype_3", "Primary_histology", "Histology_subtype_1",
                       "Histology_subtype_2", "Histology_subtype_3", "SAMPLE_NAME", "TOTAL_CN", "MINOR_ALLELE",
                       "MUT_TYPE", "GRCh"]
        TSGeneTitle = ["Chr", "Start", "End", "Gene_Symbol", "Chr_Band", "Somatic", "Germline", "Tumor_Types(Somatic)",
                       "Tumour_Types(Germline)", "Cancer_Syndrome", "Mutation_Types"]
        OncogeneTitle = ["Chr", "Start", "End", "Gene_Symbol", "Chr_Band", "Somatic", "Germline",
                         "Tumor_Types(Somatic)", "Tumour_Types(Germline)", "Cancer_Syndrome", "Mutation_Types"]
        headstr = " ".join(headlist)
        # print headlist
        if ("Chr" in headstr) or ("chr" in headstr) or ("Chromosome1" in headstr):
            # headstr.startswith("-", beg=leninput,end=len(headlist)):
            # inputlist = outputheadlist(leninput).split("\t")
            list1 = headlist[:leninput]
            line0.extend(list1)
        else:
            line0.extend("." * leninput)
        for i, j in enumerate(baselist):
            if j == "1000Genoeme":
                line0.extend(GenomeTitle)
            if j == "DGV":
                line0.extend(DGVTitle)
            if j == "dbvar":
                line0.extend(dbvarTitle)
            if j == "CNVD":
                line0.extend(CNVDTitle)
            if j == "DD1":
                line0.extend(DD1Title)
            if j == "DD2":
                line0.extend(DD2Title)
            if j == "GAD":
                line0.extend(GADTitle)
            if j == "Cosmic":
                line0.extend(CosmicTitle)
            if j == "TSGene":
                line0.extend(TSGeneTitle)
            if j == "Oncogene":
                # print True
                # print line0
                line0.extend(OncogeneTitle)
        line0.append("lable")
        # print line0
        return line0

    def run(self):

        inputFileName = self.kwargs.get('inputFileName')
        inputChrline = self.kwargs.get('inputChr')
        inputStartline = self.kwargs.get('inputStart')
        inputEndline = self.kwargs.get('inputEnd')
        # dataBase = self.kwargs.get('dataBase')
        Percent = self.kwargs.get('Percent')
        dataBaseList = self.kwargs.get('dataBase').split(',')
        # BaseList = self.kwargs.get('BaseNum').split(',')
        type = self.kwargs.get('type')
        outputFileName = self.kwargs.get('outputFileName')
        ##
        try:
            F = open(outputFileName, 'w')
        except IOError:
            print 'IO error: %s' % (outputFileName)
            sys.exit(-1)

        # ( mainLines , sampleLines) =  inputFormat.split(',')
        # outputSampeColunm = int(inputLines.split('')[0])
        fpLines = map(lambda x: int(x), [inputChrline, inputStartline, inputEndline])
        # finalOutputList = self.outLine(fpLines,len(SampleList),int(mainLines),int(sampleLines))
        # print finalOutputList
        inputInst = FileIter(inputFileName)
        # WriteListB = []
        listtable = []
        for inputItem in inputInst:
            WriteListB = []
            listlable = []
            flag = 0
            length = len(inputItem)
            WriteListB.extend(inputItem)
            for data in dataBaseList:
                data1 = self.prodatabase(data)
                dataBaseInst = FileIter(data1)
                for dataBaseItem in dataBaseInst:
                    if inputItem[fpLines[0]] == dataBaseItem[0]:
                        if int(inputItem[fpLines[1]]) <= int(dataBaseItem[1]):
                            if int(inputItem[fpLines[2]]) <= int(dataBaseItem[2]) and int(inputItem[fpLines[2]]) >= int(
                                    dataBaseItem[1]):
                                if (int(inputItem[fpLines[2]]) - int(dataBaseItem[1])) / float(
                                                int(inputItem[fpLines[2]]) - int(inputItem[fpLines[1]])) >= float(
                                        Percent):
                                    WriteListB.extend(dataBaseItem)
                                    flag = 1
                                    break
                                else:
                                    continue
                                    # WriteListB.extend("-"*len(dataBaseItem))
                            elif int(inputItem[fpLines[2]]) >= int(dataBaseItem[2]):
                                if (int(dataBaseItem[2]) - int(dataBaseItem[1])) / float(
                                                int(inputItem[fpLines[2]]) - int(inputItem[fpLines[1]])) >= float(
                                        Percent):
                                    WriteListB.extend(dataBaseItem)
                                    flag = 1
                                    break
                                else:
                                    continue
                                    # WriteListB.extend("-"*len(dataBaseItem))
                            else:
                                continue
                                # WriteListB.extend("-"*len(dataBaseItem))

                        else:
                            if int(inputItem[fpLines[2]]) >= int(dataBaseItem[2]) and int(inputItem[fpLines[1]]) <= int(
                                    dataBaseItem[2]):
                                if float(int(dataBaseItem[2]) - int(inputItem[fpLines[1]])) / float(
                                                int(inputItem[fpLines[2]]) - int(inputItem[fpLines[1]])) >= float(
                                        Percent):
                                    WriteListB.extend(dataBaseItem)
                                    flag = 1
                                    break
                                else:
                                    continue
                                    # WriteListB.extend("-"*len(dataBaseItem))
                            elif int(inputItem[fpLines[2]]) < int(dataBaseItem[2]):
                                WriteListB.extend(dataBaseItem)
                                flag = 1
                                break
                            else:
                                continue
                    elif inputItem[fpLines[0]] != dataBaseItem[0]:
                        continue
                if flag == 1:
                    listlable.append(data)
                if flag == 0:
                    WriteListB.extend("-" * len(dataBaseItem))
            if len(listlable) == 0:
                WriteListB.append("None")
            else:
                listlable1 = ",".join(listlable)
                WriteListB.append(listlable1)

            F.write('\t'.join(WriteListB) + '\n')
        F.close()
        OutputInst = FileIter(outputFileName)
        for key, outputItem in enumerate(OutputInst):
            if key == 0:
                headline = outputItem
                # print headline
                # print length
                # print dataBaseList
        head = self.addtitle(OutputInst, headline, dataBaseList, length)
        OutputInst1 = FileIter(outputFileName)

        # for i,value in enumerate(OutputInst1):
        #   if i == 0 :
        #      value =head
        #     F.write('\t'.join(value)+'\n')
        # read file to cache
        # print head
        with open(outputFileName, "r") as f1:
            lines = f1.readlines()
            # write file mode to open
        with open(outputFileName, "w") as f_w:
            for num, line in enumerate(lines):
                # if "taste" in line:
                # print line
                if num == 0:

                    # line=head
                    # print line
                    f_w.write('\t'.join(head) + '\n')

                else:
                    # print line
                    f_w.write(line)





                    #  print count


def param(argv):
    global inputfile
    global outputfile
    global db
    global percent
    global site
    try:
        options, args = getopt.getopt(argv, "hi:o:d:p:s:",
                                      ["help", "input=", "output=", "database=", "percent=", "site="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for option, value in options:
        if not option:
            usage()
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        if option in ("-i", "--input"):
            inputfile = value
        if option in ("-o", "--output"):
            outputfile = value
        if option in ("-d", "--database"):
            db = value
        if option in ("-p", "--percent"):
            percent = value
        if option in ("-s", "--site"):
            site = value
            # print (options,args)
    if args:
        print "error arrgs:%s .please input --help to get the usage" % args


def usage():
    print '''
      This program can complish CNV-ANN function.
      Options include:
        -i(--input=) inputfile,chr_pos,start_pos,end_pos   :input_file 
        -s(--site=) chr_site,start_site,end_site           :input_file's chr &star&end column from 0 
        -o(--output=) outputfile                           :output_file 
        -d(--databas=) 1000Genome,dbvar...                 :Choose CNV Annotation database ,which you want to annotate the inputfile.
                                                                There are 10 databases you can choose:
                                                                    1000Genome,DGV,dbvar,CNVD,DD1,DD2,GAD;Cosmic,TSGene,Oncogene
                                                             |---- Common CNVs  
                                                                     |-- 1000Genome 
                                                                     |-- DGV  
                                                                     |-- dbvar

                                                             |---- Diseases CNVs                                                                    
                                                                     |-- CNVD
                                                                     |-- DD1
                                                                     |-- DD2
                                                                     |-- GAD     

                                                             |---- Cancer                                            
                                                                     |-- Cosmic  
                                                                     |-- TSGene
                                                                     |-- Oncogene

        -p(--percent=)  0.3                                  :Overlap percent with the datbase which you choose. Default parameter value:0.3.                                       
        '''


def cmdDict():
    global inputfile
    global outputfile
    global db
    global percent
    global site
    sitestr = site.strip().split(",")
    callerDict = {
        'inputFileName': inputfile,
        'inputChr': sitestr[0],
        'inputStart': sitestr[1],
        'inputEnd': sitestr[2],
        'outputFileName': outputfile,
        'dataBase': db,
        'Percent': percent
    }

    return callerDict


if __name__ == '__main__':
    inputfile = ""
    outputfile = ""
    db = ""
    percent = 0.3
    site = ""
    if len(sys.argv) < 2:
        print 'please input parameters；or input --help to get the usage'
        sys.exit()
        # if sys.argv[1].startswith('--'):
        #   option = sys.argv[1][2:]
        # fetch sys.argv[1] but without the first two characters

    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        #     print callerDict
        #      print inputfile
        #      print outputfile
        #      print db
        #      print percent
        inst = allCallerSimple(**callerDict)
        inst.run()






