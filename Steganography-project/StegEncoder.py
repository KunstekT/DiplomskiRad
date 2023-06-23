import numpy as np
import cv2 as cv
import SteganographyUtils
import copy

class StegEncoder:

    def PrintEncodedMessage(self, message, colorIndex):
        colorName = "black"
        if(colorIndex == 0):
            colorName = "red"
        if(colorIndex == 1):
            colorName = "green"
        if(colorIndex == 2):
            colorName = "blue"
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~ Steganography Encoder ~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Message \""+ message +"\" encoded (last encoded pixel color: "+colorName +")")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

    def GetEncodedImage(self, image, message, printEncodedMessage = True):   
        encodedImage = copy.deepcopy(image)  
        stegUtils = SteganographyUtils.SteganographyUtils()
        binaryMessage = stegUtils.ConvertMessageToBinary(message)    
        counter = -1
        for colorIndex in range(3):
            for i in range(np.size(encodedImage, 0)):
                for j in range(np.size(encodedImage, 1)):
                    counter+=1
                    if(counter >= len(binaryMessage)):
                        if(counter == len(binaryMessage) and printEncodedMessage == True):
                            self.PrintEncodedMessage(message, colorIndex)
                    else:
                        if(binaryMessage[counter]=='1'):
                            a = encodedImage[i,j,colorIndex].astype(int) 
                            a = a | 1
                            encodedImage[i,j,colorIndex] = a
                        else:
                            a = encodedImage[i,j,colorIndex].astype(int)
                            a = a & ~1
                            encodedImage[i,j,colorIndex] = a
        if(counter < len(binaryMessage)):
            print("Warning: Message is not fully encoded.")  
        return encodedImage
