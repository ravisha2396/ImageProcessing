import numpy as np
import pandas as pd
# import cv2 as cv
from cv2 import cv2
# from google.colab.patches import cv2_imshow # for image display
from skimage import io
from PIL import Image
import matplotlib.pylab as plt
import copy
import numpy as np
import glob
import statistics

import os
from django.conf import settings


def HSV_detection(img):
    image = io.imread(img)
    image_2 = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    center_find = copy.deepcopy(image_2)
    # final_frame = cv2.hconcat((image, image_2))
    hueavg = 0
    satavg = 0
    brightavg = 0
    no_of_green = 0

    for i,image in enumerate(image_2):
        for j,img in enumerate(image):
            flag = False
            if 35<img[0]<100:
                if img[1]>60:
                    if img[2]>35:
                        hueavg += img[0]
                        satavg += img[1]
                        brightavg += img[2]
                        no_of_green += 1
                        center_find[i][j][0] = 255
                        center_find[i][j][1] = 255
                        center_find[i][j][2] = 255
                    else:
                        flag = True
                else:
                    flag = True
            else:
                flag = True
            if flag:
                center_find[i][j][0] = 0
                center_find[i][j][1] = 0
                center_find[i][j][2] = 0

    # cv2.imshow('Original image',image)
    # cv2.waitKey(0)
    # cv2.imshow('HSV image',image_2)
    # cv2.waitKey(0)
    # cv2.imshow('center find',center_find)
    # cv2.waitKey(0)
    return[hueavg/no_of_green, satavg/no_of_green, brightavg/no_of_green]
# print(center_find)
# print("Hue avg : ",hueavg/no_of_green)
# print("Sat avg : ",satavg/no_of_green)
# print("Brght avg : ",brightavg/no_of_green)

def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1], pt_1[2]))
    pt_2 = np.array((pt_2[0], pt_2[1], pt_2[2]))
    sq_dist = np.sum((pt_1-pt_2)**2, axis = 0)
    return sq_dist

def closest_node(node, nodes):
    pt = 0
    dist = 9999999
    num = 0
    for n in nodes:
        num += 1
        if distance(node, n) <= dist:
            dist = distance(node, n)
            pt = num
    return pt

# print(HSV_detection("Reference/colour-1.jpg"))
# print(HSV_detection("Reference/colour-2.jpg"))
# print(HSV_detection("Reference/colour-3.jpg"))
# print(HSV_detection("Reference/colour-4.jpg"))
# print(HSV_detection("ricecropimage1.jfif"))
try:
    ref = []
    ref1 = HSV_detection("Reference/colour-1.jpg")
    ref.append(tuple(ref1))
    ref2 = HSV_detection("Reference/colour-2.jpg")
    ref.append(tuple(ref2))
    ref3 = HSV_detection("Reference/colour-3.jpg")
    ref.append(tuple(ref3))
    ref4 = HSV_detection("Reference/colour-4.jpg")
    ref.append(tuple(ref4))
except:
    print("error")

# myLeaf = HSV_detection("ricecropimage1.jfif")
# print(closest_node(myLeaf, ref))

def image_detect(folder):
    images = glob.glob(str(folder)+"/*.jpg")
    selection = []
    for img in images:
        myLeaf = HSV_detection(img)
        selection.append(closest_node(myLeaf, ref))
    return statistics.mode(selection)

#print(image_detect("Capture1"))