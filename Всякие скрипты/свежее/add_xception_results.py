# -*- coding: utf-8 -*-

from tensorflow.keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.utils import array_to_img, img_to_array
import numpy as np
from PIL import Image


model =    load_model("Xception/weigth/10types.h5")
modelCR =  load_model("Xception/weigth/M_2хCryptomonas_Rhodomonas.h5")
modelGGP = load_model("Xception/weigth/M_3хGerodinium_Gymnodinium_Peridinium100.h5")

'''
#model.summary()
types = ['Aulacoseira','Cryptomonas','Cyclotella','Dinobryon','Gerodinium','Gymnodinium','Koliella','Peridinium','Rhodomonas','Synedra']
typesCR = ['Cryptomonas','Rhodomonas'] # 2 9
typesGGP = ['Gerodinium','Gymnodinium', 'Peridinium'] # 5 6 8
'''

#при загрузке датасета из csv
#import pandas as pd
#df = pd.read_csv('data/datasets/result/1_Ust-Barguzin/statistikDF.csv',converters={"coordinate": lambda x: list(map(float, x[1:-1].split(',')))})

#путь к файлу, координаты, путь к датасету
def xceptionUse(path, coord, path_to_result):
    path = path_to_result + '/' + path
    im = Image.open(path)

    width, height = im.size
    x,y,w,h = coord
    
    left = x*width - (w/2)*width
    top = y*height - (h/2)*height
    right = x*width + (w/2)*width
    bottom = y*height + (h/2)*height
    #вырез планктона из всего фото
    im1 = im.crop((left, top, right, bottom))
    
    #приведение фоток к размеру 299х299
    img = array_to_img(im1)
    exp_img = img.resize((299,299))
    exp_arr = img_to_array(exp_img)
    exp_arr = np.array([exp_arr])
    data_generator = image.ImageDataGenerator(rescale=1. / 255)
    test_generator = data_generator.flow(exp_arr)
    posnt = model.predict(test_generator)
    #выбор решающей сети
    if (np.argmax(posnt) == 1 or np.argmax(posnt) == 8):
        posnt = modelCR.predict(test_generator)
                    
    if (np.argmax(posnt) == 4 or np.argmax(posnt) == 5 or np.argmax(posnt) == 7):
        posnt = modelGGP.predict(test_generator)
      
    
    #возвращает номер типа и массив уверенностей
    return np.argmax(posnt), posnt
    
def mainF(df, path_to_result):
    typeXception = []
    confidencesXception = []
    for i in range(len(df)):
        print(str(df.loc[i, 'x_y']) + '/' + str(df.loc[i,'z']) + '.jpg')
        #передача x_y/путь к файлу и координаты зоны
        tempAns = xceptionUse(str(df.loc[i, 'x_y']) + '/' + str(df.loc[i,'z']) + '.jpg', df.loc[i,'coordinate'], path_to_result)
        typeXception.append(tempAns[0])
        confidencesXception.append(tempAns[1])
        
    #копия датасета
    dfXcept = df.copy()
    #добавление типа выданного xception
    dfXcept['typeXception'] = typeXception
    #добавление уверенностей xception
    dfXcept['confidencesXception'] = confidencesXception
    return dfXcept