# -*- coding: utf-8 -*-
"""
ТУТ ДАННЫЕ ИЗ ВИДА ДЛЯ YOLO ПРЕОБРАЗУЮТСЯ К ВИДУ ДЛЯ XCEPTION И ДОБАВЛЯЕТСЯ ФОН
"""
import os
from PIL import Image

#mainDir = "../../content/drive/MyDrive/yoloK/val/"
#save_dir = '/content/drive/MyDrive/test/'

def testData(mainDir, save_dir):
    labels = os.listdir(mainDir+'labels/')
    # создание папок
    сlasses = []
    for i in labels:
        myfile=open(mainDir+'labels/'+i,'r')
        lines=myfile.readlines() 
        for line in lines:
            for x in line.splitlines():
                clas = list(map(int,x.split()[:1])) #название класса из лейблов
                сlasses.append(clas[0]) # сохраняем все найденные классы

    #перебором по уникальным классам создаём папки
    for i in set(сlasses):
        os.mkdir(save_dir + str(i))
  
    j = 0
    for i in labels:
        myfile=open(mainDir+'labels/'+i,'r')
        lines=myfile.readlines()
        #print(i) # Вывод названия файла
        im = Image.open(mainDir+'images/'+i[:-4]+".jpg")
  
        for line in lines:
            for x in line.splitlines():
                cord = list(map(float,x.split()[1:])) #координаты из лейблов
                clas = list(map(int,x.split()[:1])) #название класса из лейблов
                #вырезаем по координатам планктон
                width, height = im.size
                xc1 = round(width*cord[0]) 
                yc1 = round(height*cord[1]) 
                x1 = xc1 - round(width*cord[2]/2) 
                y1 = yc1 - round(height*cord[3]/2) 
                x2 = xc1 + round(width*cord[2]/2)
                y2 = yc1 + round(height*cord[3]/2)
                cropped_img = im.crop((x1,y1,x2,y2))
                #добавление фона
                fon = Image.open('fon.jpg')
                fon.paste(cropped_img)
                fon.save(save_dir + str(clas[0])+ '/'+ str(j) + '.jpg')
                j=j+1
    return 0
                
def yoo(a, b):
    return a + b