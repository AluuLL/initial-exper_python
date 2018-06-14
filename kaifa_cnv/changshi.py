a=0
b=1
while b < 1000:
    print b,",",
    a, b = b, a+b

L1=[4,1,3,2,3,5,1]
L2=[]
[L2.append(i) for i in L1 if i not in L2]
print L2