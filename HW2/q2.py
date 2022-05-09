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
    collage = np.zeros(frame.shape[:2], dtype=np.uint8)
    modes = {0:-1}
    collage[0:block_size, 0:block_size] = 0
    
    
    for h in range(0, height, block_size):
        for w in range(0, width, block_size):

            SAD = np.inf
            mode_to_use = np.inf
            ref_block = frame[h:h+block_size, w:w+block_size]
            pred_block = np.zeros((block_size, block_size), dtype=np.int16)
            
            if h==0 and w==0:
                continue
            
            elif h==0:
                mode_to_use = 1
                ref_value = frame[h:h+block_size, w-1]
                for i, val in zip(range(block_size), ref_value):
                    pred_block[i, :] = val
                                    
            elif w==0:
                mode_to_use = 0
                ref_value = frame[h-1, w:w+block_size]
                for i, val in zip(range(block_size), ref_value):
                    pred_block[:, i] = val
                                    
            else:
                for mode in range(5):
                    local_pred_block = np.zeros((block_size, block_size), dtype=np.int16)
                    
                    if mode == 0:
                        ref_value = frame[h-1, w:w+block_size]
                        
                        for i, val in zip(range(block_size), ref_value):
                            local_pred_block[:, i] = val
                            
                        SAD_local = np.sum(np.abs(np.subtract(ref_block, local_pred_block, dtype=np.int16)))
                        if SAD_local <= SAD:
                            SAD = SAD_local
                            mode_to_use = mode
                            pred_block = local_pred_block
                        
                    elif mode == 1:
                        ref_value = frame[h:h+block_size, w-1]
                        
                        for i, val in zip(range(block_size), ref_value):
                            local_pred_block[i, :] = val
                            
                        SAD_local = np.sum(np.abs(np.subtract(ref_block, local_pred_block, dtype=np.int16)))
                        if SAD_local <= SAD:
                            SAD = SAD_local
                            mode_to_use = mode
                            pred_block = local_pred_block
                    
                    elif mode == 2:
                        ref_value = np.mean(frame[h-1, w:w+block_size] + frame[h:h+block_size, w-1], dtype=np.int16)
                        local_pred_block[:] = ref_value
                        SAD_local = np.sum(np.abs(np.subtract(ref_block, local_pred_block, dtype=np.int16)))
                        if SAD_local <= SAD:
                            SAD = SAD_local
                            mode_to_use = mode
                            pred_block = local_pred_block
                            
                    elif mode == 3:
                        continue
                    
                    elif mode == 4:
                        local_pred_block[0, :] = frame[h-1, w-1:w+block_size-1]
                        local_pred_block[:, 0] = frame[h-1:h+block_size-1, w-1]
                        
                        for i in range(1, block_size):
                            for j in range(1, block_size):
                                local_pred_block[i, j] = local_pred_block[i - 1, j - 1]
                                
                        SAD_local = np.sum(np.abs(np.subtract(ref_block, local_pred_block, dtype=np.int16)))
                        if SAD_local <= SAD:
                            SAD = SAD_local
                            mode_to_use = mode
                            pred_block = local_pred_block
                        
                    else:
                        print("Something Error!")
                        break
                
                # SAD_local = np.sum(np.abs(np.subtract(frame[h:h+block_size, w:w+block_size], ref_frame_border[h+i:h+i+block_size, w+j:w+j+block_size], dtype=np.int16)))
                # if SAD_local <= SAD:
                #     SAD = SAD_local
                #     min_vector = ((h + i - block_size) - h, (w + j - block_size) - w)
                            
            modes[int((h / block_size) * (width / block_size) + (w / block_size))] = mode_to_use
            collage[h:h+block_size, w:w+block_size] = pred_block
            
    write_to_file(os.path.join(DST_FOLDER_TXT, "modes.txt"), modes)
    return collage, modes

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
    frame_bgr = cv2.imread(os.path.join(SRC_FOLDER, 'foreman_qcif_0_rgb.bmp'))
    frame_Y, _, _ = cv2.split(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2YCrCb))
    
    cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'frame.png'), frame_Y)

    collage, _ = get_pred_modes(frame_Y)    
    cv2.imwrite(os.path.join(DST_FOLDER_IMG, 'pred_frame.png'), collage)

if __name__ == '__main__':
    main()