import pysam


tb = pysam.Tabixfile('/disk/lulu/tmp/hiseq_30x-1/hiseq_30x-1.out.cov.gz')

for item in tb.fetch('1',22975,24200):
    print (item)
    list=item.strip().split("\t")
    # print (list)
