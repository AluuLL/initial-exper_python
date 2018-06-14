from docxtpl import DocxTemplate
import time
import csv

#Variables:
date_today = time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
csvFile = open(r"/disk/lulu/autoreport/material/basicInfor.csv", "r",encoding=u'UTF-8')
reader = csv.reader(csvFile)
Name = []
Sample_ID = []
given_ID = "CM0016-2T" #给的ID

for item in reader:
    Name.append(item[1])
    Sample_ID.append(item[0])
# print (Name)
# print (Sample_ID)

if given_ID in Sample_ID:
    position = Sample_ID.index(given_ID)
realName = Name[position]
# print (rName)

csvFile.close()


doc = DocxTemplate(r"/disk/lulu/autoreport/Template.docx")
context = {'Name' : realName, 'Date' : date_today}
doc.render(context)
doc.save("generated_docyemei.docx")