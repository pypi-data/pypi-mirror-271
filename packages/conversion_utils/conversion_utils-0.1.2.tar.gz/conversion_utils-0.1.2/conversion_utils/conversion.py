import cv2
import numpy as np

class conversion:

    # def __init__(self) -> None:
    #     return

    def mask_to_bb(path):
    
        ### Read the image in gray mode
        mask_img = cv2.imread(path, 0)

        if mask_img is not None:

            mask_img_array = np.array(mask_img)

            ### Extract color
            background, mask = np.unique(mask_img_array)

            segmentation = np.where(mask_img_array == mask)

            bounding_box = 0, 0, 0, 0

            if len(segmentation) != 0:
                x_min = int(np.min(segmentation[1]))
                x_max = int(np.max(segmentation[1]))
                y_min = int(np.min(segmentation[0]))
                y_max = int(np.max(segmentation[0]))

                bounding_box = x_min, y_min, x_max, y_max
                
        return bounding_box
