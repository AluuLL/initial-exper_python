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

        # with open("/disk/lulu/Hiseq_30X_50bp-3.germ.raw.CBS") as file:
        with open(inputFileCBSName) as file:
        # f = open("out.txt", "w")
            for line in file:
                #   print line,
                list = line.strip().split("\t")
                if float(list[5]) <= (-0.5):
                    F.write(list[0] + "\t" + list[1] + "\t" + list[2] + "\t" + list[3] + "\t" + list[4] + "\t" + list[
                        5] + "\t" + list[6] + "\t" + list[7] + "\t" + list[8] + "\t" + list[9] + "\t" + list[
                              10] + "\t" + "loss"+"\n"),

                elif float(list[5]) >= 0.5:
                    F.write(list[0] + "\t" + list[1] + "\t" + list[2] + "\t" + list[3] + "\t" + list[4] + "\t" + list[
                        5] + "\t" + list[6] + "\t" + list[7] + "\t" + list[8] + "\t" + list[9] + "\t" + list[
                              10] + "\t" + "gain"+"\n"),
                else:
                    F.write(list[0] + "\t" + list[1] + "\t" + list[2] + "\t" + list[3] + "\t" + list[4] + "\t" + list[
                        5] + "\t" + list[6] + "\t" + list[7] + "\t" + list[8] + "\t" + list[9] + "\t" + list[
                              10] + "\t" + "normal"+"\n"),


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