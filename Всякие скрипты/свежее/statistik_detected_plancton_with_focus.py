# -*- coding: utf-8 -*-
import os
import math
import seaborn as sns
import pandas as pd


#df = pd.read_csv('data/datasets/result/1_Ust-Barguzin/statistikDF.csv',converters={"coordinate": lambda x: list(map(float, x[1:-1].split(',')))})
def makeGraph(path_to_result = 'D:\data\datasets\results\1_Ust-Barguzin'):
    df = pd.read_csv(path_to_result+'/statistikDF.csv',converters={"coordinate": lambda x: list(map(float, x[1:-1].split(',')))})
    dfF = find_objects(df)
    dfF = dfF.groupby('objID').max('conf')
    typenames = ['Asterionella','Aulacoseira','Aulacoseira_Is','Cryptomonas','Cyclotella','Dinobryon','Gerodinium','Gymnodinium','Koliella','Meyeri','Peridinium','Rhodomonas','Synedra']
    mapping = dict(enumerate(typenames))
    dfF['type_name'] = dfF['typeID'].map(mapping)
    sns.histplot(df, x='z', palette='rocket_r', binwidth = 1, hue='type_name', multiple='stack')
    sns.histplot(dfF, x='z', palette='rocket_r', binwidth = 1, hue='type_name', multiple='stack')
    return df,dfF


def get_statistiks(path_to_result = 'D:/data/datasets/results/10_16.09.22.Listvyanka_pribrejna_23.08.2022', xcept = False):
    x_y = [] 
    z = []
    typeId = []
    confidance = []
    coord = []
    
    #i имя папки, j имя лейблов
    # проход по папкам
    for i in os.listdir(path_to_result):
        #проход по лейблам     
        if not os.path.isfile(path_to_result+'/'+i): 
            for j in os.listdir(path_to_result+'/'+i+'/labels'):
                #проход по файлу
                with open(path_to_result+'/'+i+'/labels/'+j) as f:
                    lines = f.readlines() 
                    #проход по стокам
                    for line in lines:
                        x_y.append(i)
                        z.append(float(j[:-4]))
                        typeId.append(int(line.split(' ')[0]))
                        confidance.append(float(line.split(' ')[-1]))
                        coord.append(list(map(float, line.split(' ')[1:-1])))
    
    df = pd.DataFrame({'x_y':x_y, 'z':z,'typeID':typeId, 'confidance': confidance,'coordinate': coord})    
    #преобразование typeId к названию
    typenames = ['Asterionella','Aulacoseira','Aulacoseira_Is','Cryptomonas','Cyclotella','Dinobryon','Gerodinium','Gymnodinium','Koliella','Meyeri','Peridinium','Rhodomonas','Synedra']
    mapping = dict(enumerate(typenames))
    df['type_name'] = df['typeID'].map(mapping)
    
    df.to_csv(path_to_result + '/statistikDF.csv', index=False)  
    
    if xcept:
        import add_xception_results as axr
        axr.mainF(df, path_to_result).to_csv(path_to_result + '/statistikDFXception.csv', index=False)
    
    ## ПОИСК УНИКАЛЬНЫХ
    dfU = find_objects(df, path_to_result)
    # Отрисовка графика
    #sns.histplot(dfU, x='z', palette='rocket_r', binwidth = 1, hue='type_name', multiple='stack')
    return df, dfU

#получаем data без objID, после заполняем её none
# далее строчка на будующее, отсекаются объекты в которых objID уже указан
#while потому что не знаем сколько объектов
# объект - один физический объект, одна водросль 
#while цикл по объектам, строка в таблице - область
#один проход цикла - полное определение всех областей одного объекта
#у каждой о
#пока есть область у которой не определён объет мы будем её искать
def find_objects(data, path_to_result):
    print('Find objects')
    # Добавляем в датафрейм столбец с id объекта
    df = data.copy()
    df['objID'] = None
    df['base'] = None
    df['Distance'] = None
    
    # Создаем обрезанный датафрейм, в котором нет отмеченных объектов
    imnmark_df = df[df['objID'].isnull()].copy()
    i = 0
    
    # В цикле находим все зоны подходящие под один объект
    while len(imnmark_df) != 0:
        # Определяем первую неотмеченную зону как i объект
        # первый неотмеченный объект отмечаем номером i
        df.loc[imnmark_df.index[0],'objID'] = i
        df.loc[imnmark_df.index[0],'base'] = True
        # Убираем объекты с других x y
        imnmark_df = imnmark_df[imnmark_df['x_y']==imnmark_df.loc[imnmark_df.index[0],'x_y']]
        #получение координат базовой области
        fstcoord = getArrayAngle([imnmark_df.loc[imnmark_df.index[0],'coordinate']])        
        # Убираем слой из рассмотрения (переделать)
        imnmark_df = imnmark_df[imnmark_df['z'] != imnmark_df.loc[imnmark_df.index[0],'z']]
        
        #проход по слоям без базы
        for layer in set(imnmark_df['z']):
            layer_df = imnmark_df[imnmark_df['z'] == layer]
            # Проверяем остальные неотмеченные области на сходство
            for j in range(len(imnmark_df.loc[imnmark_df['z'] == layer])):
                scdcoord = getArrayAngle([layer_df.loc[layer_df.index[j],'coordinate']])
                # Отмечаем необходимые зоны как i объект
                (rast, distance) = compareAngle(fstcoord,scdcoord)
                
                df.loc[layer_df.index[j],'Distance'] = distance
                
                if rast:
                    df.loc[layer_df.index[j],'objID'] = i
                    #если найдена зона, то переходим на следующий фокус
                    break
                      
        # Обрезаем датафрейм, убераем отмеченные объектами зоны
        imnmark_df = df[df['objID'].isnull()].copy()
        # Увеличиваем i для следующего объекта
        i+=1
    #группирует по айди и сортирует по уверенности
    #df = df.groupby('objID').max('conf')
    unique_df = pd.DataFrame()
    #аналог groupby c сохранением осталных данных
    for i in set(df['objID']):
        temp_df = df[df['objID'] == i]
        max_conf = max(list(temp_df['confidance']))      
        unique_df = pd.concat([unique_df, temp_df[temp_df['confidance'] == max_conf]]) 
            
    unique_df.to_csv(path_to_result + '/unique.csv', index=False)
    df.to_csv(path_to_result + '/with_objID.csv', index=False)
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
    if(summa/d_arr < 0.7): 
        return True, summa/d_arr
    else: return False, summa/d_arr
    