import os
import cv2
import numpy as np

from convertYUV444to422 import convertYUV444to422
from writeToYUVFile import writeFrameToYUVFile

SRC_FOLDER = "images"


def question1():
    foreman_qcif_0_rgb = cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.bmp"))
    foreman_qcif_0_YCrCb = cv2.cvtColor(foreman_qcif_0_rgb, cv2.COLOR_BGR2YCrCb)
    foreman_qcif_0_420, _, Cr, Cb = convertYUV444to422(foreman_qcif_0_YCrCb)

    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420.bmp"), cv2.cvtColor(foreman_qcif_0_420, cv2.COLOR_YCrCb2BGR))
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Cr.bmp"), Cr)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Cb.bmp"), Cb)


def question2():
    foreman_qcif_rgb_list = []
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.bmp")))
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_1_rgb.bmp")))
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_2_rgb.bmp")))

    f = open("q2.yuv", "wb")
    for foreman_qcif_rgb in foreman_qcif_rgb_list:
        _, Y, Cr, Cb = convertYUV444to422(cv2.cvtColor(np.copy(foreman_qcif_rgb), cv2.COLOR_BGR2YCrCb))
        
        writeFrameToYUVFile(f, Y)
        writeFrameToYUVFile(f, Cb)
        writeFrameToYUVFile(f, Cr)


def main():
    question1()
    question2()


if __name__ == "__main__":
    main()