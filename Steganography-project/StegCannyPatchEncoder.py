import patchify as pf
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image
import scipy as sp

class StegCannyPatchEncoder(object):
    def GetCannyEdgesImage(self, image, n1, n2):
        edges = cv.Canny(image, n1, n2)

        threshold_value = 100
        thresholded = np.where(edges > threshold_value, 255, 0)

        thresholded = thresholded.astype(np.uint8)

        return thresholded;

    def GetEncodedImage(self, message, image, step, showPatches = False):

        image_height, image_width, channel_count = image.shape        
        patch_height, patch_width = step, step
        patch_shape = (patch_height, patch_width, channel_count)
        patches = pf.patchify(image, patch_shape, step=step)
        output_patches = np.empty(patches.shape).astype(np.uint8)
        output_canny_patches = np.empty((patches.shape[0], patches.shape[1]))
        std_values = []
        data_amount = []

        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):
                patch = patches[i, j, 0]                
                    
                std_values.append(np.std(patch))

                output_canny_patches[i, j] = self.GetCannyEdgesImage(patch, 50, 150)

                
        if(showPatches and i<1 and j<5):
            plt.figure()
            plt.imshow(cv.cvtColor(patch, cv.COLOR_BGR2RGB))
        plt.show()
        cv.waitKey(0)      

        output_height = image_height - (image_height - patch_height) % step
        output_width = image_width - (image_width - patch_width) % step
        output_shape = (output_height, output_width, channel_count)
        output_image = pf.unpatchify(output_patches, output_shape)  
        
        #output_image = Image.fromarray(output_image)
        return output_image




