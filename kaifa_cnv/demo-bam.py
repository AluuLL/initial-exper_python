import sys
import getopt
import re
from itertools import *
import time
import concurrent.futures
import pysam

bamfile = pysam.AlignmentFile('/disk/lulu/tmp/hiseq_30x-1/hiseq_30x_1.sorted.bam','rb')

value=0
count=0
pair_reads_mapq = []
pair_reads_cigarstring = []
pair_reads_mismatch = []
listread=[]
def get_n_mismatch(x):
    s = x.get_aligned_pairs(with_seq=True)
    if x.get_tag('NM') == 0:
        return 0
    n_mis = 0
    for item in s:
        if item[2] is None:
            continue
        if item[2].islower():
            n_mis = n_mis + 1
    return n_mis

for read in bamfile.fetch('1',25158688,25161509):
    # print (read.reference_start)
    # print (read.reference_end)
    # print (read.mapping_quality)
    if read.reference_start >= 25158688 and read.reference_end <= 25161509:
        value=value+(read.mapping_quality)
        count+=1
        # print read.reference_start,
        # print read.reference_end
for read in bamfile.fetch('1', 25158688 - 1000, 25158688 + 100):
    if read.next_reference_start >= (25161509 - 100) and read.next_reference_start <= (25161509 + 1000):
        pair_reads_mapq.append(read.mapq)
        pair_reads_cigarstring.append(read.cigarstring == "150M")
        pair_reads_mismatch.append(get_n_mismatch(read))

        print read
        listread.append(read)
if len(pair_reads_mapq)>0:
    pair_reads_mapq_mean = float(sum(pair_reads_mapq)) / len(pair_reads_mapq)
    pair_reads_150M_num = sum(pair_reads_cigarstring)
    pair_reads_mismatch_mean = float(sum(pair_reads_mismatch)) / len(pair_reads_mismatch)
else:
    pair_reads_mapq_mean=0
    pair_reads_150M_num=0
    pair_reads_mismatch_mean=0
print pair_reads_mapq
print pair_reads_150M_num
print pair_reads_mismatch
print len(pair_reads_mapq)

