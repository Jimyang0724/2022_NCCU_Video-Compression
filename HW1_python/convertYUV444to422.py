import cv2 
import numpy as np
# /home/jimyang/Documents/nccu/1102/vc/VC2022_HW/HW1_python

def convertYUV444to422(img_ori):
    height, width = img_ori.shape[:2]
    Y, Cr, Cb = cv2.split(np.copy(img_ori))

    Cb_sub = np.zeros((int(height/2), int(width/2)))
    Cr_sub = np.zeros((int(height/2), int(width/2)))
    
    Cb_sub[:, :] = Cb[::2, ::2] 

    Cr_sub[:, :] = Cr[::2, ::2] 

    Cb[1::2, :] = Cb[::2, :] 
    Cb[:, 1::2] = Cb[:, ::2]

    Cr[1::2, :] = Cr[::2, :] 
    Cr[:, 1::2] = Cr[:, ::2]

    return cv2.merge([Y, Cr, Cb]), Y, Cr_sub.astype(np.uint8), Cb_sub.astype(np.uint8)