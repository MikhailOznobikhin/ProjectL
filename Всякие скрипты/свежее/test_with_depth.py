# -*- coding: utf-8 -*-

#from detect import run
#import os
import pandas as pd

#либы для замера расстояния
from math import nan, isnan
import matplotlib.pyplot as plt


names_data = ["1_Ust-Barguzin","2_Froliha", "3_Listvyanka", "4_Ust-Barguzin2", "5_Nijneangarsk_21.09.14", 
             "6_Nijneangarsk_21.09.14_testRezolution/1572x1308","6_Nijneangarsk_21.09.14_testRezolution/3144x2616",
             "7_Elohin-Dovsha_15m_postoyannaya_21.06.03.testRezolution/0","7_Elohin-Dovsha_15m_postoyannaya_21.06.03.testRezolution/1","7_Elohin-Dovsha_15m_postoyannaya_21.06.03.testRezolution/2",
             "8_ Froliha_11_04_2022","9_Listvyanka_pilogeal05_05_2022/images/0", "9_Listvyanka_pilogeal05_05_2022/images/1", "9_Listvyanka_pilogeal05_05_2022/images/2"]
'''
for name in names_data:
    print(name)
    path_to_dataset = 'D:/data/datasets/'+name
    path_to_save = 'D:/data/datasets/results/'+name
    
    for i in os.listdir(path_to_dataset):
        print(i)
        if not os.path.isfile(path_to_dataset+'/'+i): 
            #nosave сохранять ли размеченные фотографии
            run(source = path_to_dataset+'/'+str(i), project = path_to_save, name = str(i), nosave=False, save_crop = True)
'''


# расстояния 
a = []
flat = []
for name in names_data:
    df = pd.read_csv('../../../data/datasets/results/'+name+'/with_objID.csv')
    sa = list(df.Distance)
    sa = [x for x in sa if isnan(x) == False]
    
    # для уникальных зон  
    #sa = [x for x in sa if x < 0.7 ]
    '''
    for i in df.query("base != True").groupby(df.objID):
        if len(i[1]) > 1:
            a.append(list(i[1].Distance))
    '''
    # для всех
    #sa = [x for x in sa if x < 1 ]
    a.append(sa)      
    
for l in a:
    for item in l:
        flat.append(item)
        
plt.hist(flat, bins=10)



#сохр в файл
from numpy import asarray
from numpy import savetxt
data = asarray(flat)
df = pd.DataFrame(data)
df.to_csv('data.csv')

#savetxt('data.csv', data, delimiter=',')