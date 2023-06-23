import patchify as pf
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import copy
#from skimage import data, io, filters

import SteganographyUtils

class StegPatchEncoder:

    def PrintEncodingStart(self, message, colorIndex):
        colorName = "black"
        if(colorIndex == 0):
            colorName = "red"
        if(colorIndex == 1):
            colorName = "green"
        if(colorIndex == 2):
            colorName = "blue"
        print("\n~~~~~~~~~~~~~~~~~~~~ Steganography Patches Encoder ~~~~~~~~~~~~~~~~~~~~")
        print("Message \""+ message +"\" encoded (last encoded pixel color: "+colorName +")")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")        
    
    def PrintMessage(self, message):        
        print(" ------------------------------------ ")
        print(" >>> "+message+" <<< ")
        print(" ------------------------------------ ")

    def Clamp(self, num, min, max):
        return min if num < min else max if num > max else num

    def GetDataAmount(self, std_value, step):
        std_value = self.Clamp(std_value, 26.0, 76.0)         
        output = (step ** 2) * (((std_value-20)/5)/12)
        return (output - output%8)

    def GetAsciiCharacter(self, binaryMessage, counter):
        x = binaryMessage[counter-8:counter]
        decimal_num = int(x, 2)  # Convert binary number to decimal
        character = chr(decimal_num)  # Convert decimal to ASCII character
        return character

    def ChangeBit(self, binaryMessage, counter, encodedPatch, i, j, colorIndex):
        if(binaryMessage[counter]=='1'):
            a = encodedPatch[i,j,colorIndex].astype(int) 
            a = a | 1
            encodedPatch[i,j,colorIndex] = a
        elif(binaryMessage[counter]=='0'):
            a = encodedPatch[i,j,colorIndex].astype(int)
            a = a & ~1
            encodedPatch[i,j,colorIndex] = a
        else:
            print("Undefined behavior... ",binaryMessage[counter])

    def EncodeMessageIntoPatch(self, patch, binaryMessage, dataAmount, currentBitCounter, addStopSigns=False, stopSign='$'):         
        encodedPatch = patch
        isFirstForLoopIteration, isDataAmountReached, isMessageFullyEncoded, isStopSignReached = True, False, False, False    
        
        counter = currentBitCounter-1
        for colorIndex in range(3):
            if(isDataAmountReached or isMessageFullyEncoded or isStopSignReached):
                break
            for i in range(np.size(encodedPatch, 0)):
                if(isDataAmountReached or isMessageFullyEncoded or isStopSignReached):
                    break
                for j in range(np.size(encodedPatch, 1)):
                    if(isDataAmountReached or isMessageFullyEncoded or isStopSignReached):
                        break
                    counter+=1
                    newDataAmount = dataAmount
                    if(newDataAmount == 0):
                        newDataAmount = 8
                    if(counter >= len(binaryMessage)):
                        isMessageFullyEncoded = True
                        break;
                    elif(counter == currentBitCounter+newDataAmount):
                        isDataAmountReached = True
                        break;
                    else:
                        if(addStopSigns and isFirstForLoopIteration==False):
                            if(counter%8==0 and counter!=0):                                
                                character = self.GetAsciiCharacter(binaryMessage, counter)
                                if(character == stopSign):
                                    isStopSignReached = True
                                    break
                        self.ChangeBit(binaryMessage, counter, encodedPatch, i, j, colorIndex)
                        isFirstForLoopIteration=False
        if(isMessageFullyEncoded):
            self.PrintMessage("MESSAGE ENCODED SUCCESSFULLY")
        currentBitCounter = counter
        return encodedPatch, currentBitCounter


#output_height = image_height - (image_height - patch_height) % step
#output_width = image_width - (image_width - patch_width) % step  
#output_shape = (output_height, output_width, channel_count)
#output_image = pf.unpatchify(output_patches, output_shape)
#output_patches_list = output_patches.reshape(-1, step, step, 3)
#min_std = np.min(std_values)
#max_std = np.max(std_values)

    def PrintMetadata(self, dataAmounts, output_patches, image, output_patches_list, std_values, min_std, max_std, step):
        print("Total data space: "+str(sum(dataAmounts))+" (ASCII characters: "+str(sum(dataAmounts)/8)+")")
        print("Number of patches: "+ str(output_patches.shape[0]*output_patches.shape[1]))
        print("image.shape: "+str(image.shape))
        print("output_patches.shape: ("+str(output_patches.shape[0])+", "+str(output_patches.shape[1])+", "+str(output_patches.shape[2])+")") 
        print("output_patches_list.size: "+str(len(output_patches_list)))
        print("output_std_deviations.size: "+str(len(std_values)))
        print("mean: "+str(sum(std_values)/len(std_values)))
        print("min_std: "+str(min_std))
        print("max_std: "+str(max_std))
        print("step: "+str(step)+", total bits available to change in a patch (single channel): "+str(step*step))

    def GetEncodedImage(self, message, image, step, addStopSigns = True, stopSign = '$'):        
        utils = SteganographyUtils.SteganographyUtils()

        image_height, image_width, channel_count = image.shape        
        patch_height, patch_width = step, step
        patch_shape = (patch_height, patch_width, channel_count)

        patches = pf.patchify(copy.deepcopy(image), patch_shape, step=step)
        std_values, dataAmounts= [], []
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):
                patch = patches[i, j, 0]
                std = np.std(patch)
                std_values.append(std)
                dataAmounts.append(self.GetDataAmount(std, step))
        
        if(addStopSigns == True):
            message = utils.AddStopSignsToMessage(message, dataAmounts, stopSign=stopSign)

        binaryMessage = utils.ConvertMessageToBinary(message)
        currentBitCounter = 0      
        encodedPatches = np.empty(patches.shape).astype(np.uint8)
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):  
                patch = patches[i, j, 0]   
                encoded_patch, currentBitCounter = self.EncodeMessageIntoPatch(
                    patch, binaryMessage, dataAmounts[i*patch.shape[0]**2+j], currentBitCounter, addStopSigns=True) 
                encodedPatches[i][j][0] = encoded_patch

        if(currentBitCounter < len(binaryMessage)):
            print("Warning: Message is not fully encoded.")          
        encoded_output_height = image_height - (image_height - patch_height) % step
        encoded_output_width = image_width - (image_width - patch_width) % step
        encoded_output_shape = (encoded_output_height, encoded_output_width, channel_count)
        encoded_output_image = pf.unpatchify(encodedPatches, encoded_output_shape)            
        return encoded_output_image


        