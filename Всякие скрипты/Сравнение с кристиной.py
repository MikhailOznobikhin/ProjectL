# -*- coding: utf-8 -*-

'''
x_y -> x, y
coordinate -> area_cx, area_cy, area_w, area_h
'''


import pandas as pd
import re
import os
import math

def x_ySplit(s):
    x,y = list(map(int,s.split('_')))
    return x,y

def x_ySplitDf(df_orig):
    df = df_orig.copy()
    x = []
    y = []
    for x_y in df.x_y:
        xi, yi = x_ySplit(x_y)
        x.append(xi)
        y.append(yi)
    df['x'] = x
    df['y'] = y
    return df

def coordSplitDf(df_orig):
    df = df_orig.copy()
    cx = []
    cy = []
    w = []
    h = []
    
    # Не помню как точно называется столбец с координатами
    # в объявлении цикла поправить мб надо
    for coord in df.coordinate:
        cx.append(float(coord[0]))
        cy.append(float(coord[1]))
        w.append(float(coord[2]))
        h.append(float(coord[3]))
    df['area_cx'] = cx
    df['area_cy'] = cy
    df['area_w'] = w
    df['area_h'] = h
    return df

def x_y2viewId(df_orig):
    df = df_orig.copy()
    x_y = list(set(df.x_y))
    xy2v = {x_y[i]:i for i in range(len(x_y))}
    df['view_id'] = [xy2v[xy] for xy in df.x_y]
    return df

def labels_to_df(path_to_result):
    x_y = [] 
    z = []
    typeId = []
    coord = []
    type_name = []
    # i имя лейбла
    # проход по лейблам
    for i in os.listdir(path_to_result):
        if os.path.isfile(path_to_result+'/'+i): 
            with open(path_to_result+'/'+i) as f:
                x_coord, y_coord, z_coord = i[:-4].split('_')
                lines = f.readlines() 
                #проход по строкам
                for line in lines:
                    x_y.append(x_coord+'_'+y_coord)
                    z.append(float(z_coord))
                    typeId.append(int(line.split(' ')[0]))
                    coord.append(list(map(float, line.split(' ')[1:])))

    df = pd.DataFrame({'x_y':x_y, 'z':z,'typeID':typeId, 'coordinate': coord}) # 'type_name':type_name})
    return df


#создание массива с углами
def getArrayAngle(arr):
    for i in arr:
        x,y,w,h = i 
        coordsAngleOneItem = [x-w/2,y+h/2, x+w/2,y+h/2, x+w/2,y-h/2, x-w/2, y-h/2]
        #округление координат до 7 знаков после запятой
        coordsAngleOneItemRound = [round(cord, 7) for cord in coordsAngleOneItem] 
    return coordsAngleOneItemRound

#сравнение координат вершин возвращает суммарную разницу вершин
def compareAngle(arr1, arr2):
    summa = 0
    #проход по координатам всех углов
    for i in range(4):
        summa += math.sqrt(math.pow(arr1[i*2]-arr2[i*2],2) + math.pow(arr1[i*2+1]-arr2[i*2+1],2))
    
    d_arr1 = math.sqrt(math.pow(arr1[0]-arr1[4],2) + math.pow(arr1[1]-arr1[5],2))
    d_arr2 = math.sqrt(math.pow(arr2[0]-arr2[4],2) + math.pow(arr2[1]-arr2[5],2))
    d_arr = min(d_arr1, d_arr2)
    
    #если уверенность меньше то возвращаем, что они разные  
    #print(summa/d_arr)
    if(summa/d_arr < 1.8): 
        return True, summa/d_arr
    else: return False, summa/d_arr




df = pd.read_csv('D:/data/datasets/results/2_Froliha/unique.csv' ,converters={"coordinate": lambda x: list(map(float, x[1:-1].split(',')))})

x_y = [str(i)+'_'+str(j) for i in range(10) for j in range(15)]
coordinate = [(i,j,i/7,j/6) for i in range(10) for j in range(15)]

# Тестовый датафрем - заменить на рабочий
#df = pd.DataFrame({'x_y':x_y,'coordinate':coordinate})

df1 = x_ySplitDf(df)
df1 = coordSplitDf(df1)
#print(df1)


df2 = labels_to_df('E:/Работа ЛИМ/РАБОТА/работа с разметкой кристины по глубине/Для разметки/22 03 10 Фролиха_21 09 14/Метки')
df2 = df2[df2.typeID < 13]
df2['handle'] = True
df2.index = list(range(len(df2)))

df2 = x_ySplitDf(df2)
df2 = coordSplitDf(df2)

#x, y, координаты сети, координаты кристины, уверенность сети, класс сети, класс кристины
dfAll = df2.copy()
dfAll= dfAll.drop(columns  = ['x_y', 'coordinate', 'z', 'handle'])
dfAll = dfAll.rename( columns = {'typeID' : 'Handle_class', 'area_cx': 'Handle_cx',
                      'area_cy': 'Handle_cy','area_w': 'Handle_w',
                      'area_h': 'Handle_h'})
dfAll['Yolo_cx'] = None
dfAll['Yolo_cy'] = None
dfAll['Yolo_w'] = None
dfAll['Yolo_h'] = None
dfAll['Yolo_confidance'] = None
dfAll['Yolo_class'] = None
dfAll['pair'] = False

dfYolo = df1.copy()

for i, s in df2.iterrows():
    srav = dfYolo[dfYolo.x_y == s.x_y]
    for jj, j in srav.iterrows():
        firs = getArrayAngle([s.coordinate])
        secd = getArrayAngle([j.coordinate])
        camp, rast = compareAngle(firs, secd)
        if camp:
            dfAll.loc[i, 'Yolo_cx'] = j.area_cx
            dfAll.loc[i, 'Yolo_cy'] = j.area_cy
            dfAll.loc[i, 'Yolo_w'] = j.area_w
            dfAll.loc[i, 'Yolo_h'] = j.area_h
            dfAll.loc[i, 'Yolo_confidance'] = j.confidance
            dfAll.loc[i, 'Yolo_class'] = j.typeID
            dfAll.loc[i, 'pair'] = True
            dfYolo = dfYolo.drop(index = jj)
            break
       
dfYolo['Handle_class'] = None
dfYolo['Handle_cx'] = None
dfYolo['Handle_cy'] = None
dfYolo['Handle_w'] = None
dfYolo['Handle_h'] = None
dfYolo['pair'] = False
dfYolo= dfYolo.drop(columns  = ['x_y', 'coordinate', 'z', 'objID','base','type_name','Distance'])
dfYolo = dfYolo.rename( columns = {'typeID' : 'Yolo_class', 'area_cx': 'Yolo_cx',
                      'area_cy': 'Yolo_cy','area_w': 'Yolo_w',
                      'area_h': 'Yolo_h', 'confidance':'Yolo_confidance'
                         })

dfYolo.index = [i for i in range(max(dfAll.index)+1, max(dfAll.index)+1+len(dfYolo))]

dfRez = pd.concat([dfAll, dfYolo])
dfRez.to_csv('2_Froliha.csv')
print(len(dfRez[dfRez.pair]))