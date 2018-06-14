import sys
import getopt


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
        # with open("/disk/lulu/Hiseq_30X_50bp-3.germ.0.5.sort.CBS") as file:
        with open(inputFileCBSName) as file:
            global listprint
            listprint = []
            for line in file:
                list = line.strip().split("\t")
                for i, j in enumerate(list):
                    if listprint:
                        # print (list[1],listprint[1],list[10],listprint[10])
                        if list[1] == listprint[1] and list[10] == listprint[10]:
                            listprint[3] = list[3]
                            if list[4] != "NA":
                                listprint[4] = str(float((float(list[4]) + float(listprint[4])) / 2))
                            # listprint[4]=str(int((int(list[4])+int(listprint[4]))/2))
                            if list[5] != "NA":
                                listprint[5] = str((float(list[5]) + float(list[5])) / 2)
                            if list[6] != "NA":
                                listprint[6] = str((float(list[6]) + float(list[6])) / 2)
                            if list[7] != "NA":
                                listprint[7] = str((float(list[7]) + float(list[7])) / 2)
                            if list[8] != "NA":
                                listprint[8] = str((float(list[8]) + float(list[8])) / 2)
                            if list[9] != "NA":
                                listprint[9] = str((float(list[9]) + float(list[9])) / 2)
                        else:
                            F.write("\t".join(listprint))
                            F.write("\n")
                            listprint = list
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