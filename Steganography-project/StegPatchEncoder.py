from turtle import color
from uu import encode
import patchify as pf
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import copy

import SteganographyUtils
import StegDecoder

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

    def EncodeMessageIntoPatch(self, patch, colorIndex, binaryMessage, dataAmount, currentBitCounter, addStopSigns=False, stopSign='$'):
        encodedPatch = patch
        isFirstForLoopIteration, isDataAmountReached, isMessageFullyEncoded, isStopSignReached = True, False, False, False
        counter = currentBitCounter-1
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

    def GetDataAmount(self, std_value, step):
        std_value = self.Clamp(std_value, 26.0, 76.0)         
        output = (step ** 2) * (((std_value-20)/5)/12)
        return (output - output%8)

    def GetChannelDataAmounts(self, patches, step, channel):
        dataAmounts = []
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):                            
                patch = patches[i, j, 0]
                std = np.std(patch[:,:,channel])
                dataAmounts.append(self.GetDataAmount(std, step))
        return dataAmounts

    def GetDataAmounts(self, patches, step):
        dataAmountsR, dataAmountsG, dataAmountsB = [], [], []
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):                              
                patch = patches[i, j, 0]
                stdR = np.std(patch[:,:,2])
                stdG = np.std(patch[:,:,1])
                stdB = np.std(patch[:,:,0])
                dataAmountsR.append(self.GetDataAmount(stdR, step))
                dataAmountsG.append(self.GetDataAmount(stdG, step))
                dataAmountsB.append(self.GetDataAmount(stdB, step))
        return [dataAmountsB, dataAmountsG, dataAmountsR] 

    def GetEncodedImage(self, message, image, step, channel=0, addStopSigns = True, stopSign = '$'):        
        utils = SteganographyUtils.SteganographyUtils()
        image_height, image_width, channel_count = image.shape        
        patch_height, patch_width = step, step
        patch_shape = (patch_height, patch_width, channel_count)
        patches = pf.patchify(copy.deepcopy(image), patch_shape, step=step)                                             #dataAmountsTotal = self.GetDataAmounts(patches, step) 
        dataAmounts = self.GetChannelDataAmounts(patches, step, channel)                                                 #dataAmounts = dataAmountsTotal[channel]        
        if(addStopSigns == True):                                                                                       #message = utils.AddStopSignsToMessage(message, dataAmountsTotal[channel], stopSign=stopSign) 
            message = utils.AddStopSignsToMessage(message, dataAmounts, stopSign=stopSign) 
        binaryMessage = utils.ConvertMessageToBinary(message)

        currentBitCounter = 0 
        encodedPatches = np.empty(patches.shape).astype(np.uint8)
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):  
                patch = patches[i, j, 0]                                
                encoded_patch, currentBitCounter = self.EncodeMessageIntoPatch(patch, channel, binaryMessage, 
                    dataAmounts[int(i*image_width/patch.shape[0]+j)], currentBitCounter, addStopSigns=addStopSigns)                
                encodedPatches[i][j][0] = encoded_patch

        if(currentBitCounter < len(binaryMessage)):
            print("Warning: Message is not fully encoded.")

        encoded_output_height = image_height - (image_height - patch_height) % step
        encoded_output_width = image_width - (image_width - patch_width) % step
        encoded_output_shape = (encoded_output_height, encoded_output_width, channel_count)
        encoded_output_image = pf.unpatchify(encodedPatches, encoded_output_shape)            
        return encoded_output_image


        