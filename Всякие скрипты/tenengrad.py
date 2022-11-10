# -*- coding: utf-8 -*-
from skimage import filters
import os
import cv2
import numpy as np
from skimage import filters
import os

main_dir = 'D:/yolov5/data/data/testFocus3'
labels = os.listdir(main_dir)
sharpents = [] 

#размеры изображения
img_width = 3488
img_height = 2616
count_y = 3#3 6  12 24
count_x = 4#4 #8 16 32 
height = int(img_height / count_y)
width  = int(img_width / count_x)

def tenengrad(reImg):
    img2gray = cv2.cvtColor(reImg, cv2.COLOR_BGR2GRAY)
    f = np.matrix(img2gray)
    tmp = filters.sobel(f)
    source=np.sum(tmp**2)
    source=np.sqrt(source)
    return source

#одну фотку получаем сегметы
#получаем массив для чёткости для сегментов одной фотки
#выход двумерный массив
def segments(reImg):
    sharpent = np.zeros((count_y,count_x))
    for y in range(count_y):
        for x in range(count_x):
            segment = reImg[y*height:y*height+height, x*width:x*width+width]
            sharpent[y,x] = tenengrad(segment)
            print(sharpent)
    return sharpent

def createImg(imgs, argmx):
    img = reImg
    for y in range(count_y):
        for x in range(count_x):
            img[y*height:y*height+height, x*width:x*width+width] = imgs[argmx[y,x]][y*height:y*height+height, x*width:x*width+width]
    return img

imgs = []
for i in labels:
  reImg = cv2.imread(main_dir+i)
  sharpents.append(segments(reImg))
  imgs.append(reImg)   
        
#объединениие в кучу
#reImg[2*y:2*y+height, x:x+width] = reImg[y:y+height, x:x+width]
# Show image
#cv2.imshow("cropped", createImg(imgs, np.argmax(sharpents,0)))
cv2.imwrite('D:/yo.jpg', createImg(imgs, np.argmax(sharpents,0)))
print(np.argmax(sharpents,0))
#cv2.waitKey(0)

