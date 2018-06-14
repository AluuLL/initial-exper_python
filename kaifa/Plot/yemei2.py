from docxtpl import DocxTemplate
import time
import csv
import os
import codecs
from docxtpl import DocxTemplate
import time
import csv
####解决了中文问题
#Variables:
Name = []
Sample_ID = []
given_ID = "CM0016-2T" #给的ID

date_today = time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
csvFile = codecs.open("/disk/lulu/autoreport/material/basicInfor.csv","r",'gbk')
reader = csv.DictReader(csvFile)
for row in reader:
    print (row)
    Name.append(row['姓名'])
    Sample_ID.append(row['样本编号'])

if given_ID in Sample_ID:
    position = Sample_ID.index(given_ID)
realName = Name[position]

csvFile.close()

doc = DocxTemplate(r"/disk/lulu/autoreport/template.docx")
context = {'name' : realName, 'report_date' : date_today}
doc.render(context)
doc.save("/disk/lulu/autoreport/generated_doctest.docx")
