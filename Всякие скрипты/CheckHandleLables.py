import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from math import floor, ceil
import os
import time

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
                x_coord,y_coord,z_coord = i[:-4].split('_')
                lines = f.readlines() 
                #проход по строкам
                for line in lines:
                    x_y.append(x_coord+'_'+y_coord)
                    z.append(int(z_coord))
                    typeId.append(int(line.split(' ')[0]))
                    coord.append(list(map(float, line.split(' ')[1:])))
    
    df = pd.DataFrame({'x_y':x_y, 'z':z,'typeID':typeId, 'coordinate': coord}) # 'type_name':type_name})
    return df

def normCoord2pxCoordCorner(coord, imgsize):
    xc = coord[0]
    yc = coord[1]
    w = coord[2]
    h = coord[3]
    
    x1 = xc - w/2
    x2 = xc + w/2
    y1 = yc - h/2
    y2 = yc + h/2
    
    px_x1 = ceil(x1*imgsize[0])
    px_x2 = floor(x2*imgsize[0])
    px_y1 = ceil(y1*imgsize[1])
    px_y2 = floor(y2*imgsize[1])
    
    if px_x1 < 0:
        px_x1 = 0
    if px_x2 > imgsize[0]:
        px_x2 = imgsize[0]
    if px_y1 < 0:
        px_y1 = 0
    if px_y2 > imgsize[1]:
        px_y2 = imgsize[1]
    
    pxCoord = [px_x1, px_y1, px_x2, px_y2]
    
    return pxCoord
    
def label2img(imgpath, df):
    img = Image.open(imgpath)
    img = img.convert("RGBA")
    
    fnt = ImageFont.truetype("courbd.ttf", 30)

    for i in range(len(df)):
        tmp = Image.new('RGBA', img.size, (0,0,0,0))
        draw = ImageDraw.Draw(tmp)
        text = df.loc[i, 'type_name']
        pxCoord = df.loc[i, 'pxCoordCorner']
        x1 = pxCoord[0]
        y1 = pxCoord[1]
        x2 = pxCoord[2]
        y2 = pxCoord[3]
        
        if not df.loc[i,'handle']:
            draw.rectangle(((x1,y1), (x2,y2)), fill=(255,0,0,70), outline=(255,0,0,255), width = 3)
            draw.rectangle(((x1,y1), (x1+18*len(text)+4,y1-20-4)), fill=(255,0,0,255))
            draw.text((x1+2,y1-28), text, fill = (255,255,255,255), font = fnt)
        else:
            draw.rectangle(((x1,y1), (x2,y2)), fill=(0,0,255,70), outline=(0,0,255,255), width = 3)
            draw.rectangle(((x1,y2), (x1+18*len(text)+4,y2+20+4)), fill=(0,0,255,255))
            draw.text((x1+2,y2-4), text, fill = (255,255,255,255), font = fnt)
            
        img = Image.alpha_composite(img, tmp)
    return img

pd.options.display.max_rows = 1000
pd.options.display.max_columns = 10
tn = ['Asterionella','Aulacoseira','Aulacoseira_Is','Cryptomonas','Cyclotella','Dinobryon','Gerodinium','Gymnodinium','Koliella','Meyeri','Peridinium','Rhodomonas','Synedra']
imgsize = (3488,2616)

df = pd.read_csv('C:/Users/Эрик/Downloads/4_Ust-bargusin_2_osadok.csv' ,converters={"coordinate": lambda x: list(map(float, x[1:-1].split(',')))})
df1 = df[['x_y','z','typeID','coordinate']]
df1.z = df1.z.astype(int)
df1['handle'] = False
df1['pxCoordCorner'] = None
pxCoords = []
for i in range(len(df1)):
    pxCoords.append(normCoord2pxCoordCorner(df1.loc[i,'coordinate'], imgsize))
df1['pxCoordCorner'] = pxCoords

df2 = labels_to_df('C:/Users/Эрик/Downloads/Кристина разметка/Для разметки/22 03 15 Усть-Баргузин_7км_центральный разрез_22 02 25/Метки')
df2 = df2[df2.typeID < 13]
df2['handle'] = True
df2['pxCoordCorner'] = None
df2.index = list(range(len(df2)))
pxCoords = []
for i in range(len(df2)):
    pxCoords.append(normCoord2pxCoordCorner(df2.loc[i,'coordinate'], imgsize))
df2['pxCoordCorner'] = pxCoords



testdf = pd.concat([df1, df2])
testdf.index = list(range(len(testdf)))
testdf['type_name'] = None
tns = []
for i in range(len(testdf)):
    tns.append(tn[testdf.loc[i,'typeID']])
testdf['type_name'] = tns
testdf['x_y_z'] = testdf['x_y'] + '_' + testdf['z'].astype(str)

photopath = 'E:/ЛИМ Фото/4_Ust-Barguzin2'
resultpath = 'E:/ЛИМ Фото/4_Усть-Баргузин_сравнение'

for xyz in set(testdf['x_y_z']):
    tmpdf = testdf[testdf['x_y_z'] == xyz]
    tmpdf.index = list(range(len(tmpdf)))
    x,y,z = xyz.split('_')
    xy = x+'_'+y 
    imgpath = photopath + '/' + xy + '/' + z +'.jpg'

    img = label2img(imgpath, tmpdf)
    img.convert('RGB').save(resultpath+'/'+xyz+'.jpg')

#stimg = label2img(path, testdf)
