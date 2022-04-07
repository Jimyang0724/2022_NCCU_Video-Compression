import os
import cv2
import copy
import numpy as np

from convertYUV444to422 import convertYUV444to422

SRC_FOLDER = "images"

def question1():
    foreman_qcif_0_rgb = cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.bmp"))
    foreman_qcif_0_YCrCb = cv2.cvtColor(foreman_qcif_0_rgb, cv2.COLOR_BGR2YCrCb)
    foreman_qcif_0_420 = convertYUV444to422(foreman_qcif_0_YCrCb)
    _, Cr, Cb = cv2.split(foreman_qcif_0_420)

    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420.bmp"), cv2.cvtColor(foreman_qcif_0_420, cv2.COLOR_YCrCb2BGR))
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Cr.bmp"), Cr)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Cb.bmp"), Cb)


    cv2.imshow("ORI", cv2.cvtColor(foreman_qcif_0_420, cv2.COLOR_YCrCb2BGR))
    cv2.waitKey(0)

def main():
    question1()

if __name__ == "__main__":
    main()