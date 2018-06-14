from docxtpl import DocxTemplate
#coding=utf-8

# doc = DocxTemplate("/disk/lulu/autoreport/header_footer_tpl.docx")  # 对要操作的docx文档进行初始化
# context = {'company_name': "World company",'title':"Lulu"}  # company_name 是存在于1.docx文档里面的变量，就像这样{{company_name}}，直接放在1.docx文件的明确位置就行
# doc.render(context)  # 这里是有jinjia2的模板语言进行变量的替换，然后便可以在1.docx文档里面看到{{company_name}}变成了World company
# doc.save("/disk/lulu/autoreport/generated_doc.docx")  # 保存
doc = DocxTemplate("/disk/lulu/autoreport/template.docx")
context = {
            #'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
            'tbl_contents': [
                {'label': 'yellow', 'cols': ['MAP6D1', '1', 'c.45C>T', 'p.R15R', u'同义突变', '67.86%']},
                {'label': 'red', 'cols': ['ZNF628', '3', 'c.700A>G', 'p.T234A', u'非同义突变', '61.46%']},
                {'label': 'green', 'cols': ['C2orf72', '1', 'c.36T>C', 'p.L12L', u'同义突变', '55.10%']},
                {'label': 'green', 'cols': ['ZIC5', '1', 'c.1254G>A', 'p.P418P', u'同义突变', '45.00%']},

            ],
            'indel_contents': [
                {'label': 'yellow', 'cols': ['MAP6D1', '1', 'c.45C>T', 'p.R15R', u'同义突变', '67.86%']},
                {'label': 'red', 'cols': ['ZNF628', '3', 'c.700A>G', 'p.T234A', u'非同义突变', '61.46%']},
                {'label': 'green', 'cols': ['C2orf72', '1', 'c.36T>C', 'p.L12L', u'同义突变', '55.10%']},
                {'label': 'green', 'cols': ['ZIC5', '1', 'c.1254G>A', 'p.P418P', u'同义突变', '45.00%']},

            ],
            'cnv_contents': [
                {'value': ['ANKRD18A', u'拷贝数增加', '3']},
                {'value': ['CCDC73', u'拷贝数增加', '3']},
                {'value': ['CTSS', u'拷贝数增加', '3']},
                {'value': ['DUSP9', u'拷贝数增加', '3']},
                {'value': ['DUX4', u'拷贝数减少', '1']},
                {'value': ['FAM58A', u'拷贝数增加', '3']},
            ]
        }
doc.render(context)
doc.save("/disk/lulu/autoreport/generated_doc.docx")
