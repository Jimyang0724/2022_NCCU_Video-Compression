import os
import cv2
import numpy as np

SRC_FOLDER = './image_input'
DST_FOLDER_IMG = './q1_output/image_output'
DST_FOLDER_TXT = './q1_output/txt_output'

def write_to_file(path, file):
    with open(path, 'w') as f:
        for index in file:
            f.write(f"Block {str(index)} – {str(file[index])}\n")

def get_motionVector(ref_frame, frame, block_size=16):
    height, width = frame.shape[:2]
    MVs = {}
    
    ref_frame_border = cv2.copyMakeBorder(
        ref_frame, 
        top     = block_size, 
        bottom  = block_size, 
        left    = block_size,
        right   = block_size,
        borderType = cv2.BORDER_REPLICATE
    )
    
    for h in range(0, height, block_size):
        for w in range(0, width, block_size):

            min_vector = (0, 0)
            SAD = np.inf
            for i in range(32):
                for j in range(32):
                    SAD_local = np.sum(np.abs(np.subtract(frame[h:h+block_size, w:w+block_size], ref_frame_border[h+i:h+i+block_size, w+j:w+j+block_size], dtype=np.int16)))
                    if SAD_local <= SAD:
                        SAD = SAD_local
                        min_vector = ((h + i - block_size) - h, (w + j - block_size) - w)
                        
            MVs[int((h / block_size) * (width / block_size) + (w / block_size))] = min_vector
                    

    write_to_file(os.path.join(DST_FOLDER_TXT, "motion_vector.txt"), MVs)
    return MVs

def make_collage(ref_frame, MVs, block_size=16):
    height, width = ref_frame.shape[:2]
    pred_frame = np.zeros(ref_frame.shape, dtype=np.uint8)
    ref_frame_border = cv2.copyMakeBorder(
        ref_frame, 
        top     = block_size, 
        bottom  = block_size, 
        left    = block_size,
        right   = block_size,
        borderType = cv2.BORDER_REPLICATE
    )
    
    for h in range(0, height, block_size):
        for w in range(0, width, block_size):
            MV = MVs[int((h / block_size) * (width / block_size) + (w / block_size))]
            pred_frame[h:h+16, w:w+16] = ref_frame_border[(h + MV[0] + 16):(h + MV[0] + 32), (w + MV[1] + 16):(w + MV[1] + 32)]
    
    return pred_frame
    
def main():
    ref_frame_bgr = cv2.imread(os.path.join(SRC_FOLDER, 'foreman_qcif_0_rgb.bmp'))
    frame_bgr = cv2.imread(os.path.join(SRC_FOLDER, 'foreman_qcif_1_rgb.bmp'))
    
    ref_frame_Y, _, _ = cv2.split(cv2.cvtColor(ref_frame_bgr, cv2.COLOR_BGR2YCrCb))
    frame_Y, _, _ = cv2.split(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2YCrCb))
    
    cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'ref_frame.png'), ref_frame_Y)
    cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'cur_frame.png'), frame_Y)

    MVs = get_motionVector(ref_frame_Y, frame_Y)
    pred_frame = make_collage(ref_frame_Y, MVs)
    
    cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'collage_frame.png'), pred_frame)

if __name__ == '__main__':
    main()