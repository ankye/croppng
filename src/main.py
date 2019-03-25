# -*- coding: utf-8 -*-

import argparse
import os
import sys
import os.path
import shutil
from PIL import Image
import json
import numpy as np
import cv2
from skimage import io,data

def createDestDir(destDir):
    curPath = os.getcwd()  # 当前路径
    aim_path = os.path.join(curPath, destDir)
    print(aim_path)
    if os.path.isdir(aim_path):
        shutil.rmtree(aim_path, True)  # 如果有该目录,删除
    os.makedirs(aim_path)
    return aim_path

def crop(destDir,x,y,w,h,png):
    
    rbx = x+w
    rby = y+h
    result_image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rect_on_big = srcImage.crop((x, y, rbx, rby))
    result_image.paste(rect_on_big, (0, 0, w, h))
    result_image.save(destDir+'/'+png)


parser = argparse.ArgumentParser()
parser.add_argument("--png")
parser.add_argument("--out")
args = parser.parse_args()

fileName = args.png
dest = args.out

if fileName.find('.png') != -1:
    fileName = fileName[:-4]

pngName = fileName + '.png'
destDir = createDestDir(dest)

srcImage = Image.open(pngName)

img = srcImage.convert('RGBA')
frames = []
L,H=img.size 
for h in range(H):
    for l in range(L):
        dot = (l,h)
        rgba = img.getpixel(dot)
        if(rgba[0] != 0 or rgba[1] != 0 or rgba[2] != 0 or rgba[3] != 0):
            img.putpixel(dot,(255,255,255,255))
        else:
            img.putpixel(dot,(0,0,0,0))
img2 = img.convert('L')
img2.save("temp/test1.jpg")


# 原始图像real
real = cv2.imread('temp/test1.jpg')

gray = cv2.cvtColor(real,cv2.COLOR_BGR2GRAY)  
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
  
contours, hierarchy = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
cv2.drawContours(real,contours,-1,(0,0,255),3)  
#print(contours[0])

for i in range(0,len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    cv2.rectangle(real, (x,y), (x+w,y+h), (153,153,0), 5) 
    frames.append([x,y,w,h])

io.imsave('temp/img.jpg',real)

for i in range(0,len(frames)):
    frame = frames[i]
    name = str(i) + ".png"
    crop(destDir,frame[0],frame[1],frame[2],frame[3],name)


del srcImage




