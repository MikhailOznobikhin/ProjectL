# -*- coding: utf-8 -*-
import os
import math
import numpy as np
from PIL import Image


labelDir = "test/labels/"
'''надо везде заменить labels[0] на лейбл в котором максимум объектов'''

#чтение txt файлов, стартовая функция
def read_files(labelDir):
    labels = os.listdir(labelDir)
    #labels.remove('ResMerge.txt') # Для повторного запуска не рассматривать предыдущий результат
    
    # генерация словаря название файла : массив найденных в нём видов
    all_files = dict.fromkeys(labels)
    kind = dict.fromkeys(labels) # номер вида
    
    #вид   y-коорд   х-коорд    ширина  высота  уверенность
    coords = []
    
    for file_name in labels:
        with open(labelDir+file_name) as f:
            lines = f.readlines() 
            kind_list = [] #временноая переменная хранит список видов
            for i in lines:
                #выбираем координаты и добавляем их в общий массив
                coords.append(list(map(float, i.split()[1:5])))
                #сохраняем вид
                kind_list.append(int(i.split()[0]))
            kind[file_name] = kind_list 
        ## преобразуем массив с координатами x,y, ширина, высота в координаты углов
        all_files[file_name] = getArrayAngle(coords)
        coords = []
        
    #получение базы
    base = get_base(all_files, labels)
    newPlancton = [] #массив в котором хранятся новые обнаруженные объекты
       
    for i in all_files:
        #передаём массив координат базы, название не базы, вид, массив всех лейблов 
        print('compareArray')
        newPlancton.append(compareArray(base.get(next(iter(base))), i, kind, all_files))
        #print('Внешняя итерация: ', i)
        
        # compareArray при отсутствии совпадений возвращает пустой массив
        ''' newPlankton возвращал массив пустых массивов '''
        for i in newPlancton:
            for j in i:
                if j != []: # раньге было без цикла по i и было if i != [], но i было = [[],[]]
                    print('newL^ ', i)
                    arr = base.get(labels[0])
                    arr.append(i[0])
        newPlancton = [] # обнуление чтобы не залетало 2 одинаковых
    
    save_in_file(base, labelDir)    
    return all_files, base


#создание массива с углами
def getArrayAngle(arr):
    coordsAngle = [] #x0 x1 y0 y1
    for i in arr:
        x,y,w,h = i
        coordsAngleOneItem = [x-w/2, x+w/2, y - h/2, y + h/2]      
        #округление координат до 5 знаков после запятой
        coordsAngleOneItemRound = [round(cord, 5) for cord in coordsAngleOneItem] 
        coordsAngle.append(coordsAngleOneItemRound)
    return coordsAngle


#получение базового снимка на котором больше всего объектов, потом с ним сравниваются остальные
def get_base(all_files, labels):
    count_fito = []
    for i in all_files.values():
        count_fito.append(len(i)) 
    #получаем индекс с наибольшим количеством объектов, берём его из лейблов и вытаскиваем массив из словаря
    base = {labels[np.argmax(count_fito)] : all_files[labels[np.argmax(count_fito)]]}    
    #удаление из общего словаря
    all_files.pop(labels[np.argmax(count_fito)])
    return base


#сравнение координат вершин возвращает суммарную разницу вершин
def compareAngle(arr1, arr2):
    #корень квадрата разницы
    a1 = math.sqrt( math.pow(arr1[0]-arr2[0],2))
    a2 = math.sqrt( math.pow(arr1[1]-arr2[1],2))
    a3 = math.sqrt( math.pow(arr1[2]-arr2[2],2))
    a4 = math.sqrt( math.pow(arr1[3]-arr2[3],2))
    return a1 + a2 + a3 + a4


#сравнение массивов массивов    
def compareArray(base, name, kind, all_files):
    main = [] #сохраняется совпадение объекта из второго с элементами первого
    res = [] #массив сравнений одного элемента второго массива со всеми первого
    without_base = [] # отсутствующие на базе
    without_base_kind = [] # отсутствующий на базе, виды
    
    for a in all_files.get(name):
        print('base: ', base)
        for b in base: #ОШИБКА в arr1
            #ТУТ сравнение по относительным координатам
            #Задание коэффициента     
            print('a: ', a)
            print('b: ', b)
            if(compareAngle(a,b) < 0.05):
                res.append(0)
            else:
                res.append(1)
        
        if 0 in res: main.append(0)     #совпадает с одним из
        if 0 not in res: main.append(1) #нужо добавить в базу
        res = []
    
    for i in range(len(main)):
        if main[i] == 1:
            without_base.append(all_files.get(name)[i])
            without_base_kind.append(kind.get(name)[i])
            
    return without_base, without_base_kind



def save_in_file(dict_base, labelDir):
    f = open(labelDir + 'ResMerge.txt', 'w')
    values_base = dict_base.get(next(iter(dict_base)))
    #f.write(str(dict_base.get(next(iter(dict_base)))))
    for value in values_base:
        #print(value)
        f.write(str(value) + '\n')
    f.close()
    
            
# максимальная разница между всеми, то это всё один объект




'''
снимок где больше всего объектов взять за базу
дальше следующий снимок и сравниваем их между собой и добавляем его в основную

отдельная функция для сравнения по виду

один за базу и дальше по одиночке
'''    

#лишнее, не идёт в продашн
'''    
#тест на открытие и проверку координат        
x,y,w,h = coords[6]

import cv2   
img_width = 3488
img_height = 2616

img = cv2.imread('test/002-0007.jpg')

#вычисление координат
xStart = int(x*img_width - (w * img_width)/2)
xEnd = int(x*img_width + (w * img_width)/2)
yStart = int(y*img_height - (h * img_height)/2)
yEnd = int(y*img_height + (h * img_height)/2)

cv2.imshow("cropped", img[yStart:yEnd, xStart : xEnd] )
cv2.waitKey(0)
cv2.destroyAllWindows()

'''