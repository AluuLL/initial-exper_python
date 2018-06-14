import sys
import getopt
import re
from itertools import *
import time


class allCallerSimple():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        inputFileCBSName = self.kwargs.get('inputFileCBSName')
        outputFileName = self.kwargs.get('outputFileName')
        ##
        try:
            F = open(outputFileName, 'w')
        except IOError:
            print ('IO error: %s' % (outputFileName))
            sys.exit(-1)

        with open(inputFileCBSName) as file:
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
                        num = num + 1
                        if float(listprint[22]) >= 0.8:
                            count = count + 1
                        if list[1] == listprint[1] and list[2] == listprint[2] and list[3] == listprint[3]:
                            flag = 1
                            num = num + 1
                            if float(list[22]) >= 0.8:
                                count = count + 1
                                listprint = list
                        else:
                            flag = 0
                            ratio = count / num
                            if ratio >= 0.7:
                                # print("\t".join(listprint))
                                F.write("\t".join(listprint))
                                F.write("\n")
                                listprint = list
                                count = 0
                                num = 0
                            else:
                                listprint = list
                                count = 0
                                num = 0

                    else:
                        if list[1] == listprint[1] and list[2] == listprint[2] and list[3] == listprint[3]:
                            flag = 1
                            num = num + 1
                            if float(list[22]) >= 0.8:
                                count = count + 1
                                listprint = list
                        else:
                            flag = 0

                            ratio = count / num
                            if ratio >= 0.7:
                                # print("\t".join(listprint))
                                F.write("\t".join(listprint))
                                F.write("\n")
                                listprint = list
                                count = 0
                                num = 0
                            else:
                                listprint = list
                                count = 0
                                num = 0
                else:
                    listprint = list

        F.close()



def param(argv):
    global inputfile_CBS
    global outputfile

    try:
        options, args = getopt.getopt(argv, "hi:o:",
                                      ["help", "inputCBS=","output="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for option, value in options:
        if not option:
            usage()
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        if option in ("-i", "--inputCBS"):
            inputfile_CBS = value
        if option in ("-o", "--output"):
            outputfile = value

            # print (options,args)
    if args:
        print ("error arrgs:%s .please input --help to get the usage" % args)


def usage():
    print ('''
      This program can complish CBS file's surrounding depth caculate function.
      Options include:
        -i(--inputCBS=) input .CBS file                    :inputCBSfile 
        -o(--output=) outputfile                           :output_file                                      
        ''')


def cmdDict():
    global inputfile_CBS
    global outputfile
    # global percent
    # global site
    # sitestr = site.strip().split(",")
    callerDict = {
        'inputFileCBSName': inputfile_CBS,
        'outputFileName': outputfile,
    }

    return callerDict


if __name__ == '__main__':
    inputfile_CBS = "" #输入待求的CBS文件
    outputfile = ""    #输出文件名
    #percent = 0.3

    if len(sys.argv) < 2:
        print ('please input parameters；or input --help to get the usage')
        sys.exit()
        # if sys.argv[1].startswith('--'):
        #   option = sys.argv[1][2:]
        # fetch sys.argv[1] but without the first two characters

    else:
        param(sys.argv[1:])
        callerDict = cmdDict()
        #     print callerDict
        inst = allCallerSimple(**callerDict)
        inst.run()