# -*- coding: utf-8 -*-

import argparse
import os
import sys
import os.path
import shutil
from PIL import Image
import json

parser = argparse.ArgumentParser()
parser.add_argument("--name")
args = parser.parse_args()

fileName = args.name

if fileName.find('.png') != -1:
    fileName = fileName[:-4]

pngName = fileName + '.png'
atlasName = fileName + '.atlas'

print(pngName, atlasName)

big_image = Image.open(pngName)


curPath = os.getcwd()  # 当前路径
aim_path = os.path.join(curPath, fileName)
print(aim_path)
if os.path.isdir(aim_path):
    shutil.rmtree(aim_path, True)  # 如果有该目录,删除
os.makedirs(aim_path)
#
content = ""
with open(atlasName, encoding='utf-8') as fp:
    while True:
        c = fp.readline()
        if len(c) == 0:
            break
        content += c

data = json.loads(content)

for k in data["frames"].keys():
    print(k)
    #{'frame': {'x': 572, 'y': 668, 'w': 260, 'h': 127, 'idx': 0}, 'spriteSourceSize': {'x': 68, 'y': 226}, 'sourceSize': {'w': 500, 'h': 500}}
    frame = data["frames"][k]["frame"]
    print(data["frames"][k])
    width = frame["w"]
    height = frame["h"]
    ltx = frame["x"]
    lty = frame["y"]
    rbx = ltx+width
    rby = lty+height
    result_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rect_on_big = big_image.crop((ltx, lty, rbx, rby))
    result_image.paste(rect_on_big, (0, 0, width, height))
    result_image.save(aim_path+'/'+k)

del big_image
