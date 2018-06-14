import os
from pysam import VariantFile
#file = open("sample.txt")
#for line in file:
#   print line,

vcf_in = VariantFile("/disk/lulu/database/1000Genome/ALL.chr5.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf")
vcf_out = VariantFile('-','w',header=vcf_in.header)

for rec in vcf_in.fetch():
   # print (rec.info.values())
  print (rec.info["SVTYPE"])
#    print (rec.chrom)
#    print (rec.pos)
#    print (rec.id)
#    print (rec.ref)
 #   print (rec.ALT)
#    print (rec.qual)
#    print list(rec.filter)
#    print list(rec.format)
# #   print (vcf_in.header)


##  print (rec.type,rec.key)