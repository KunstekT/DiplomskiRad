import numpy as np
import cv2 as cv
import patchify as pf
import matplotlib.pyplot as plt
import copy
#import SteganographyUtils
import StegDecoder

class StegPatchDecoder:
           
    def Decode(self, image, step, decodeUntilStopSign = False, stopSign='$'):   
        stegDecoder = StegDecoder.StegDecoder()        
        
        image_height, image_width, channel_count = image.shape        
        patch_height, patch_width = step, step
        patch_shape = (patch_height, patch_width, channel_count)
        patches = pf.patchify(copy.deepcopy(image) , patch_shape, step=step)

        output_patches = np.empty(patches.shape).astype(np.uint8)
        output_messages = []

        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):
                patch = patches[i, j, 0] 
                hiddenMessage = stegDecoder.Decode(patch, decodeUntilStopSign=decodeUntilStopSign, stopSign=stopSign)
                output_messages.append(hiddenMessage)
                output_patches[i, j, 0] = patch
        
        output_message = "".join(output_messages)
        return output_message



