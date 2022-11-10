# -*- coding: utf-8 -*-
from detect import run

import os

dir_to_source = 'D:/data/datasets/10_16.09.22.Listvyanka_pribrejna_23.08.2022/'
save_dir = 'D:/data/datasets/results/10_16.09.22.Listvyanka_pribrejna_23.08.2022/'

#mainDir = "/content/yolov5/runs/detect/exp2/labels"
#mainDir директория с лейблами от yolo

def coun_true(mainDir, clas):
    print(mainDir)
    true_count = 0 #количество верных ответов
    labels = os.listdir(mainDir)

    for i in labels:
        myfile=open(mainDir+'/'+i,'r')
        lines=myfile.readlines()
        if str(lines[0].split(' ')[0]) == str(clas):
            true_count = true_count + 1
    return true_count, len(labels)

'''
for i in os.listdir(dir_to_source):
    print(i)
    run(source = dir_to_source+i+'/', project = save_dir)
    #true_count, labels_count = coun_true('scripts/yolo/'+i+'/exp/labels', i)
    #trues_all.append(true_count)
    #labels_for_all.append(labels_count) 
'''
#labels_for_all
'''

'''
def text(x):
    return f'{(x-1) // 10}_{(x-1) % 10}'    

for name in os.listdir(save_dir):
    os.rename(save_dir+name, save_dir+text(int(name[3:])))


'''    
for j in range(50):
    for i in range(10):
        print(j)
        for di in f:
            name = 'exp'+str(di)
            os.rename(save_dir+name, save_dir+str(j)+'_'+str(i))
 
'''