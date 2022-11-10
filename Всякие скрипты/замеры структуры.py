# -*- coding: utf-8 -*-

import os


labels = os.listdir('labels')
arr = []
for i in labels:
    with open('labels/'+i) as f:
        lines = f.readlines() 
        #проход по стокам
        for line in lines:
            arr.append(int(line[:2]))
            

a = 0
for j in arr:
    if(j == 1):
        a+=1
print(a)