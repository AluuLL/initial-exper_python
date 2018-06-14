#coding=utf-8
import requests
s=requests

###init

# data ={"labelData":"{'性别': [], '年龄': [], '病理诊断': [],'病人批次': []}"}
data ={"accurate":"{'病人批次': ['20180420','2']}"}
# data = {"accurate": "{'病人批次': ['1','12']}"}
r=s.post('http://192.168.75.251:8686/accurate',data)


##interact
#data={"kaks_mean":"较高"}


##genete word
#data={"report_id":1}
#r=s.post('http://192.168.75.251:8686/generate_word',data)
#r=s.post('http://192.168.75.251:8686/report_interact',data)
print(r.text)