import cv2
import os

SRC_PATH = "./Result_img"
DST_PATH = "./Result_img"

files = os.listdir(SRC_PATH)
print(files)
for file in files:
    if file[-3:] == "bmp":
        src = os.path.join(SRC_PATH, file)
        dst = os.path.join(DST_PATH, f"{file[:-4]}.jpg")
        img = cv2.imread(src)
        cv2.imwrite(dst, img)
        print(dst)