from ast import Pass
from imp import new_module
from uu import encode
import patchify as pf
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image
import scipy as sp
import copy
#from skimage import data, io, filters

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
    def Clamp(self, num, min, max):
        return min if num < min else max if num > max else num

    def GetDataAmount(self, std_value, step):

        #print((step ** 2)*(std_value/80)*12) # TODO: (?) benceviceva formula 

        #std_value = self.Clamp(std_value, 26.0, 81.0) # Removed MAX possibe data because of stop sign addition
        std_value = self.Clamp(std_value, 26.0, 76.0)         
        output = (step ** 2) * (((std_value-20)/5)/12)

        #print("output: ",output-output%8," (",std_value,", ",int((std_value-20)/5),")")
        return (output - output%8)

    def EncodeMessageIntoPatch(self, patch, binaryMessage, dataAmount, currentBitCounter, addStopSigns=False, stopSign='$'):    
        
        isFirstForLoopIteration = True
        encodedPatch = patch
        isDataAmountReached = False
        isMessageFullyEncoded = False
        isStopSignReached = False
        encodedMessage = "" # used only to print
        
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
                                x=""+str(binaryMessage[counter-8])+str(binaryMessage[counter-7])+str(binaryMessage[counter-6])+str(binaryMessage[counter-5])+str(binaryMessage[counter-4])+str(binaryMessage[counter-3])+str(binaryMessage[counter-2])+str(binaryMessage[counter-1])
                                decimal_num = int(x, 2)  # Convert binary number to decimal
                                character = chr(decimal_num)  # Convert decimal to ASCII character
                                #print("character: "+character);
                                if(character == stopSign):
                                    isStopSignReached = True
                                    break
                                    #print("stop sign '",stopSign,"' reached! ")
                                else:
                                    #print("not reached")
                                    pass
                        if(binaryMessage[counter]=='1'):
                            encodedMessage += "1"
                            a = encodedPatch[i,j,colorIndex].astype(int) 
                            a = a | 1
                            encodedPatch[i,j,colorIndex] = a
                        elif(binaryMessage[counter]=='0'):
                            encodedMessage += "0"
                            a = encodedPatch[i,j,colorIndex].astype(int)
                            a = a & ~1
                            encodedPatch[i,j,colorIndex] = a
                        else:
                            print("Undefined behavior... ",binaryMessage[counter])
                        isFirstForLoopIteration=False

        if(isDataAmountReached):
            pass
            #print("DataAmount is reached! Counter progress: ", counter-currentBitCounter, "Total: ",counter)
        if(isMessageFullyEncoded):
            print(" ------------------------------------ ")
            print(" >>> MESSAGE ENCODED SUCCESSFULLY <<< ")
            print(" ------------------------------------ ")
        if(isStopSignReached):
            #print("Reached '",stopSign,"', message: ",encodedMessage)
            pass


        currentBitCounter = counter
        return encodedPatch, currentBitCounter

    def GetEncodedImage(self, message, image, step, addStopSigns = True, stopSign = '$', showPatches = False, printMetadata=False):
        utils = SteganographyUtils.SteganographyUtils()

        image_height, image_width, channel_count = image.shape        
        patch_height, patch_width = step, step
        patch_shape = (patch_height, patch_width, channel_count)

        img=copy.deepcopy(image)        

        patches = pf.patchify(img, patch_shape, step=step)
        output_patches = np.empty(patches.shape).astype(np.uint8)
        std_values = []
        dataAmounts = []
        decoder = StegDecoder.StegDecoder()

        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):
                patch = patches[i, j, 0]                
                
                if(showPatches):
                    plt.figure()
                    plt.imshow(cv.cvtColor(patch, cv.COLOR_BGR2RGB))

                std_values.append(np.std(patch))
                output_patches[i, j, 0] = patch

        #cv.waitKey(0)        

        for i in range(len(std_values)):
            dataAmounts.append(self.GetDataAmount(std_values[i], step))
            #print(str(i)+": "+str(data_amount[i])+" ("+str(std_values[i])+")")
            
        output_height = image_height - (image_height - patch_height) % step
        output_width = image_width - (image_width - patch_width) % step
        output_shape = (output_height, output_width, channel_count)
        output_image = pf.unpatchify(output_patches, output_shape)        
        
        
        output_patches_list = output_patches.reshape(-1, step, step, 3)
       
        if(showPatches):
            plt.figure()
            plt.imshow(cv.cvtColor(output_patches_list[0], cv.COLOR_BGR2RGB))
            plt.imshow(cv.cvtColor(output_patches_list[1], cv.COLOR_BGR2RGB))
            plt.imshow(cv.cvtColor(output_patches_list[2], cv.COLOR_BGR2RGB))

        min_std = np.min(std_values)
        max_std = np.max(std_values)

        if(printMetadata):
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

        #print(str(output_patches_list[127])+"\n--------------\n"+str(output_patches[0][127][0]))
        #print(str(output_patches_list[128])+"\n--------------\n"+str(output_patches[1][0][0]))
        
        if(addStopSigns == True):
            newMessage="";
            newMessage = utils.AddStopSignsToMessage(message, dataAmounts, stopSign=stopSign)
            message = newMessage;   

        binaryMessage = utils.GetBinaryMessageString(message)
        currentBitCounter = 0
        
        print("DataAmounts: ",dataAmounts[:10])
        encodedPatches = np.empty(patches.shape).astype(np.uint8)
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):  
                patch = patches[i, j, 0]   
                encoded_patch, currentBitCounter = self.EncodeMessageIntoPatch(patch, binaryMessage, dataAmounts[i*patch.shape[0]**2+j], currentBitCounter, addStopSigns=True)                    
                
                #if(currentBitCounter <400):
                #    stegDecoder = StegDecoder.StegDecoder()
                #    x = stegDecoder.Decode(encoded_patch, showMessage=True, decodeUntilStopSign=True, messageFilter=False)
                #    print(x)
                    
                encodedPatches[i][j][0] = encoded_patch

                x = decoder.Decode(encoded_patch, decodeUntilStopSign=True)

                if(i<2 and j<512):
                    if(x != ""):        
                        print("i: ",i,", j: ",j)
                        print(x[:10])
                        print("----------")

        if(currentBitCounter < len(binaryMessage)):
            print("Warning: Message is not fully encoded.")  
        
        encoded_output_height = image_height - (image_height - patch_height) % step
        encoded_output_width = image_width - (image_width - patch_width) % step
        encoded_output_shape = (encoded_output_height, encoded_output_width, channel_count)
        encoded_output_image = pf.unpatchify(encodedPatches, encoded_output_shape)

        #print("encoded_output_image: ",encoded_output_image)
        #stegDecoder = StegDecoder.StegDecoder()
        #x = stegDecoder.Decode(encoded_output_image, showMessage=True, decodeUntilStopSign=True, messageFilter=False)
        #print(x)


        if(showPatches):              
            plt.show()
            
        #output_image = Image.fromarray(output_image)
        #output_image.save("output.jpg")
        return encoded_output_image


        