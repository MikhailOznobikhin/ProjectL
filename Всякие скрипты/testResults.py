# -*- coding: utf-8 -*-

import os
from PIL import Image

#mainDir = "/content/yolov5/runs/detect/exp2/labels"
#mainDir директория с лейблами от yolo
def coun_true(mainDir):
    true_count = 0 #количество верных ответов
    labels = os.listdir(mainDir)

    for i in labels:
        myfile=open(mainDir+'/'+i,'r')
        lines=myfile.readlines()
        if str(lines[0][:1]) == '0':
            true_count = true_count + 1
    
    return true_count, len(labels)