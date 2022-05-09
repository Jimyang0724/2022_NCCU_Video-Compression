import os
import cv2
import numpy as np

SRC_FOLDER = './image_input'
DST_FOLDER_IMG = './q2_output/image_output'
DST_FOLDER_TXT = './q2_output/txt_output'

def write_to_file(path, file):
    with open(path, 'w') as f:
        for index in file:
            f.write(f"Block {str(index)} – {str(file[index])}\n")

def get_pred_modes(frame, block_size=16):
    height, width = frame.shape[:2]
    modes = {}
    
    for h in range(16, height, block_size):
        for w in range(16, width, block_size):

            SAD = np.inf
            ref_frame = frame[h:h+block_size, w:w+block_size]
            pred_frame = np.zeros((block_size, block_size), dtype=np.int16)

            for mode in range(5):
                if mode == 0:
                    ref_value = frame[h-1, w:w+block_size]
                    for i, val in zip(range(block_size), ref_value):
                        pred_frame[:, i] = val
                    SAD_local = np.sum(np.abs(np.subtract(ref_frame, pred_frame, dtype=np.int16)))
                    if SAD_local <= SAD:
                        SAD = SAD_local
                    
                elif mode == 1:
                    ref_value = frame[h:h+block_size, w-1]
                    for i, val in zip(range(block_size), ref_value):
                        pred_frame[i, :] = val
                    SAD_local = np.sum(np.abs(np.subtract(ref_frame, pred_frame, dtype=np.int16)))
                    if SAD_local <= SAD:
                        SAD = SAD_local
                
                elif mode == 2:
                    ref_value = np.mean(frame[h-1, w:w+block_size] + frame[h:h+block_size, w-1], dtype=np.int16)
                    pred_frame[:] = ref_value
                    SAD_local = np.sum(np.abs(np.subtract(ref_frame, pred_frame, dtype=np.int16)))
                    if SAD_local <= SAD:
                        SAD = SAD_local                 
                        
                elif mode == 3:
                    continue
                
                elif mode == 4:
                    ref_value = frame[h-1, w-1:w+block_size]
                    ref_value = np.concatenate(([ref_value], [frame[h-1:h+block_size, w-1]]))
                    for i in range(block_size):
                        for j in range(block_size):
                            pred_frame[i, j] = 
                    # print(ref_value)
                    # print(pred_frame)
                    # print()

                
                else:
                    continue
                
                # SAD_local = np.sum(np.abs(np.subtract(frame[h:h+block_size, w:w+block_size], ref_frame_border[h+i:h+i+block_size, w+j:w+j+block_size], dtype=np.int16)))
                # if SAD_local <= SAD:
                #     SAD = SAD_local
                #     min_vector = ((h + i - block_size) - h, (w + j - block_size) - w)
                            
            modes[int((h / block_size) * (width / block_size) + (w / block_size))] = mode
                    

    write_to_file(os.path.join(DST_FOLDER_TXT, "modes.txt"), modes)
    return modes

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
    # ref_frame_bgr = cv2.imread(os.path.join(SRC_FOLDER, 'foreman_qcif_0_rgb.bmp'))
    frame_bgr = cv2.imread(os.path.join(SRC_FOLDER, 'foreman_qcif_1_rgb.bmp'))
    
    # ref_frame_Y, _, _ = cv2.split(cv2.cvtColor(ref_frame_bgr, cv2.COLOR_BGR2YCrCb))
    frame_Y, _, _ = cv2.split(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2YCrCb))
    
    # cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'ref_frame.png'), ref_frame_Y)
    cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'cur_frame.png'), frame_Y)

    modes = get_pred_modes(frame_Y)
    # pred_frame = make_collage(ref_frame_Y, MVs)
    
    # cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'pred_frame.png'), pred_frame)

if __name__ == '__main__':
    main()