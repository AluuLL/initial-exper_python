import os
from sys import argv
import re
import vcf
a = argv[1]
vcf_reader = vcf.Reader(filename=r'a')
for record in vcf_reader:
        print record.CHROM,
        print record.POS,
        print record.ID,
        print record.REF,
        print record.ALT,
        if 'CS' in record.INFO.keys():
            print record.INFO['CS'],
        else:
            print "None",
        if 'END' in record.INFO.keys():
            print record.INFO['END'],
        else:
            print "None",

        if 'IMPRECISE' in record.INFO.keys():
            print record.INFO['IMPRECISE'],
        else:
            print "FAlSE",
        if 'SVTYPE' in record.INFO.keys():
            print record.INFO['SVTYPE'],
        else:
            print "None",
        print record.INFO['AC'],
        print record.INFO['AF'],
        print record.INFO['NS'],
        print record.INFO['AN'],
        print record.INFO['EAS_AF'],
        print record.INFO['EUR_AF'],
        print record.INFO['AFR_AF'],
        print record.INFO['AMR_AF'],
        print record.INFO['SAS_AF'],
        print record.INFO['DP']

