import os
from sys import argv
import re
import vcf
a = argv[1]
vcf_reader = vcf.Reader(filename=a)
for record in vcf_reader:
        print record.CHROM,"\t",
        print record.POS,"\t",
        # print (record.ID,"\t",)
        # print (record.REF,"\t",)
        # print (record.ALT,"\t",)
        # if 'CS' in record.INFO.keys():
        #     print (record.INFO['CS'],"\t",)
        # else:
        #     print ("None","\t",)
        if 'END' in record.INFO.keys():
            print record.INFO['END'],"\t",
        else:
            print "None","\t",

#         if 'IMPRECISE' in record.INFO.keys():
#             print (record.INFO['IMPRECISE'],"\t",)
#         else:
#             print ("FAlSE","\t",)
#         if 'SVTYPE' in record.INFO.keys():
#             print (record.INFO['SVTYPE'],"\t",)
#         else:
#             print ("None","\t",)
#         print (record.INFO['AC'],"\t",)
#         print (record.INFO['AF'],"\t",)
#         print (record.INFO['NS'],"\t",)
#         print (record.INFO['AN'],"\t",)
#         print (record.INFO['EAS_AF'],"\t",)
#         print (record.INFO['EUR_AF'],"\t",)
#         print (record.INFO['AFR_AF'],"\t",)
#         print (record.INFO['AMR_AF'],"\t",)
#         print (record.INFO['SAS_AF'],"\t",)
# #        print record.INFO['DP']
#         if 'DP' in record.INFO.keys():
#             print (record.INFO['DP'])
#         else:
#             print ("None")