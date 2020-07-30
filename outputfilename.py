import os

filePath = "D:\Program Files (x86)"
a = []
### 
for i,j,k in os.walk(filePath):
    for b in k:
       a.append(b) 
print(a)

with open("fileName.txt",'w',encoding='utf-8') as fp:
    print("ready")
    i = 0
    for b in a:
        fp.write(b + '\n')
        print("写入第{}行".format(i))
        i = i + 1
    print("OK!")
    fp.close()
