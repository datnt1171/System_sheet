# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 08:29:05 2024

@author: KT1
"""

import cv2


def image_resize(image, width = None, height = None, inter = cv2.INTER_LANCZOS4):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

image_path = r'C:\Users\KT1\Downloads\image\old\212 FINISHING SYSTEM (Aug 05, 2024)_SUA.png'
des = r'C:\Users\KT1\Downloads\image\old\aaaa.png'
temp = cv2.imread(image_path)
temp1 = image_resize(temp, width=550, height=None)
cv2.imwrite(des, temp1)

image_new_path = [] # take the excel_file path
image_path_list = [] # get all image in image folder
for image_path in image_path_list:
    image = cv2.imread(image_path)
    image = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(image_path, image)