import os
import cv2
import numpy as np

from convertYUV444to420 import convertYUV444to420
from writeToFile import writeFrameToYUVFile, writeStrToFile
from quantizer import Quantizer
from huffman_coding import HuffmanCoding

SRC_FOLDER = "./images"
FRAME_HEIGHT = 144
FRAME_WIDTH = 176


def question1():
    foreman_qcif_0_rgb = cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.bmp"))
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.jpg"), foreman_qcif_0_rgb)
    
    foreman_qcif_0_YCrCb = cv2.cvtColor(foreman_qcif_0_rgb, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(foreman_qcif_0_YCrCb)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_Y.jpg"), Y)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_Cr.jpg"), Cr)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_Cb.jpg"), Cb)
    
    foreman_qcif_0_420, Y, Cr, Cb = convertYUV444to420(foreman_qcif_0_YCrCb)

    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420.jpg"), cv2.cvtColor(foreman_qcif_0_420, cv2.COLOR_YCrCb2BGR))
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Y.jpg"), Y)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Cr.jpg"), Cr)
    cv2.imwrite(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb_420_Cb.jpg"), Cb)


def question2():
    foreman_qcif_rgb_list = []
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.bmp")))
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_1_rgb.bmp")))
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_2_rgb.bmp")))

    f = open("./yuvs/q2.yuv", "wb")
    for foreman_qcif_rgb in foreman_qcif_rgb_list:
        _, Y, Cr, Cb = convertYUV444to420(cv2.cvtColor(np.copy(foreman_qcif_rgb), cv2.COLOR_BGR2YCrCb))
        
        writeFrameToYUVFile(f, Y)
        writeFrameToYUVFile(f, Cb)
        writeFrameToYUVFile(f, Cr)


def question3():
    foreman_qcif_rgb_list = []
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_0_rgb.bmp")))
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_1_rgb.bmp")))
    foreman_qcif_rgb_list.append(cv2.imread(os.path.join(SRC_FOLDER, "foreman_qcif_2_rgb.bmp")))

    Ys = []
    Crs = []
    Cbs = []
    for foreman_qcif_rgb in foreman_qcif_rgb_list:
        _, Y, Cr, Cb = convertYUV444to420(cv2.cvtColor(np.copy(foreman_qcif_rgb), cv2.COLOR_BGR2YCrCb))
        Ys.append(Y)
        Crs.append(Cr)
        Cbs.append(Cb)
    
    quantizer = Quantizer(Ys, Crs, Cbs, n_intensity=8)
    huffman = HuffmanCoding()
    quantizer.quantization()
    qYs, qCrs, qCbs = quantizer.getQ()
    
    stream = np.array([])
    for id in range(len(qYs)):
        stream = np.append(stream, np.concatenate((qYs[id].flatten(), qCbs[id].flatten(), qCrs[id].flatten())))
        
    encodeStream = huffman.encode(stream)
    f = open("q3_encoded_bitstream.txt", "w")
    writeStrToFile(f, encodeStream)
    
    decodeStream = huffman.decode(encodeStream)
    
    nqYs = np.copy(qYs)
    nqCrs = np.copy(qCrs)
    nqCbs = np.copy(qCbs)
    
    offset = int(len(decodeStream)/3)
    for id in range(len(qYs)):
        yOffset = int(((offset)/6)*4)
        cOffset = int((offset)/6)
        yRaw = decodeStream[int(id*offset):int(id*offset+yOffset)]
        cbRaw = decodeStream[int(id*offset+yOffset):int(id*offset+yOffset+cOffset)]
        crRaw = decodeStream[int(id*offset+yOffset+cOffset):int(id*offset+yOffset+cOffset*2)]
        for i in range(FRAME_HEIGHT):
            for j in range(FRAME_WIDTH):
                nqYs[id][i, j] = yRaw[i*FRAME_WIDTH+j]
        for i in range(int(FRAME_HEIGHT/2)):
            for j in range(int(FRAME_WIDTH/2)):
                nqCrs[id][i, j] = crRaw[i*int(FRAME_WIDTH/2)+j]
                nqCbs[id][i, j] = cbRaw[i*int(FRAME_WIDTH/2)+j]
    
    quantizer.setQs(nqYs, nqCrs, nqCbs)
    quantizer.dequantization()
    dqYs, dqCrs, dqCbs = quantizer.getDQ()
    
    f = open("./yuvs/q3.yuv", "wb")
    for id in range(len(qYs)):
        writeFrameToYUVFile(f, dqYs[id].astype(np.uint8))
        writeFrameToYUVFile(f, dqCbs[id].astype(np.uint8))
        writeFrameToYUVFile(f, dqCrs[id].astype(np.uint8))

def main():
    question1()
    question2()
    question3()


if __name__ == "__main__":
    main()