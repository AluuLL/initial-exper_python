#coding=utf-8
import requests
s=requests

###init
##data={"性别":["男","女"],"年龄":[50,60],"病理诊断":["非小细胞肺癌","小细胞癌","肺腺癌","腺鳞癌"],"病人批次":["2018.01.01","2018.01.10"]}

#data ={"labelData":"{'性别': [], '年龄': [], '病理诊断': [],'病人批次': []}"}
# r=s.post('http://192.168.75.251:8686/label_search',data)
r=s.post('http://192.168.75.251:8686/usage_statistics')
##interact
#data={"kaks_mean":"较高"}


##genete word
#data={"report_id":1}
#r=s.post('http://192.168.75.251:8686/generate_word',data)
#r=s.post('http://192.168.75.251:8686/report_interact',data)
print(r.text)