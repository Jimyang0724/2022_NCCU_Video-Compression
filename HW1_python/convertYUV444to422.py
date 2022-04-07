import cv2 
import copy
import numpy as np
# /home/jimyang/Documents/nccu/1102/vc/VC2022_HW/HW1_python

def convertYUV444to422(img_ori):
    # height, width = img_ori.shape[:2]
    Y, Cr, Cb = cv2.split(img_ori)

    Cb_sub = np.copy(Cb)
    Cr_sub = np.copy(Cr)
    
    Cb_sub[1::2, :] = Cb_sub[::2, :] 
    Cb_sub[:, 1::2] = Cb_sub[:, ::2]

    Cr_sub[1::2, :] = Cr_sub[::2, :] 
    Cr_sub[:, 1::2] = Cr_sub[:, ::2]

    return cv2.merge([Y, Cr_sub, Cb_sub])
    # return Y, Cr_sub, Cb_sub