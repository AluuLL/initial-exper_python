
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

list1=[]
with open("/disk/lulu/process/banchmark.txt","r") as filea:
    list10=[]
    for i in filea:
        list10=i.strip()
        list1.append(int(list10))

print (list1)

# list2=[4,5,6]
# list3=[7,8,9]
# datafram= pd.DataFrame({"a":list1,"b":list2,"c":list3})
# print (datafram)

# data=pd.read_csv('*.csv')