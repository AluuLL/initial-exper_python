import pysam

def get_region_value(file):
    with open(file, 'r') as regionFile :
        region_value = []
        for line in regionFile:
             line_value = line.strip().split("\t")
             line_value[1] = int(line_value[1])
             line_value[2] = int(line_value[2])
             region_value.append(line_value)
    regionFile.close()
    return (region_value)

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

bamfile = pysam.AlignmentFile("/disk/zhanglu/zhonghuayihao/hg38-zhonghuayihao/NIST/NIST1/Quartet_DNA_ILM_ARD_NIST8398_1_20170403.sorted.bam","rb")

file = "/disk/chenfs/Project/zhonghua_SV/result/NIST/Select_SV_new/new/test.region.txt"


region_values = get_region_value(file)


read_mapq =  []
read_cigarstring = []
read_mismatch = []
for read in bamfile.fetch("chr11", 58453151 - 1000, 58453151 + 100):
    if read.next_reference_start > 58453462 - 100 and read.next_reference_start <  58453462 + 1000:
        read_mapq.append(read.mapq)
        read_cigarstring.append(read.cigarstring == "150M")
        read_mismatch.append(get_n_mismatch(read))

read_mapq_mean = float(sum(read_mapq)) / len(read_mapq)
read_cigar_150M_num = sum(read_cigarstring)
read_mismatch_mean = float(sum(read_mismatch)) / len(read_mismatch)