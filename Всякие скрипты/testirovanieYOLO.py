# -*- coding: utf-8 -*-
"""
в данном файле объединяются данные с тестирвоания йоло из txt в датафрейм
"""

import pandas as pd
import os

typenames = ['Asterionella','Aulacoseira','Aulacoseira_Is','Cryptomonas','Cyclotella','Dinobryon','Gerodinium','Gymnodinium','Koliella','Meyeri','Peridinium','Rhodomonas','Synedra']
pat = 'D:/google drive/DatasetXception-20220309T144126Z-001/result/'
d = {'src':[]
        ,'class_yolo':[]
        ,'class_real':[]}

for directory in os.listdir(pat):
    print(pat+directory+'/labels')
    for file in  os.listdir(pat+directory+'/labels'):
        with open(pat+directory+'/labels/'+file) as f:
            lines = f.readlines() 
            for line in lines:
                d['src'].append(pat+directory+'/labels/'+file)
                d['class_yolo'].append(int(line.split(' ')[0]))
                d['class_real'].append(int(directory))
    
df = pd.DataFrame(d)
L = [[0 for i in range(13)] for j in range(13)]
for i in range(len(df)):
    L[df.loc[i,'class_real']][df.loc[i,'class_yolo']] += 1


#df.to_csv('D:/google drive/datasetXceptionForYoloUpscaleAllUse-20220309T115404Z-001/statistikDF.csv', index=False)    


#888 261 1165 987 547 296 496 384 696 311 448