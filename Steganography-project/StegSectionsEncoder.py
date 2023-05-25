import numpy as np
import cv2 as cv
import SteganographyUtils

class StegSectionsEncoder:

    def PrintEncodingStart(self, message, colorIndex):
        colorName = "black"
        if(colorIndex == 0):
            colorName = "red"
        if(colorIndex == 1):
            colorName = "green"
        if(colorIndex == 2):
            colorName = "blue"
        print("\n~~~~~~~~~~~~~~~~~~~~ Steganography Sections Encoder ~~~~~~~~~~~~~~~~~~~~")
        print("Message \""+ message +"\" encoded (last encoded pixel color: "+colorName +")")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

    def GetImageSections(self, image, sectionLength):
        ary = np.array(image)
        return np.split(ary, sectionLength, axis=0)

    def GetEncodedImage(self, image, message, numberOfSections, showEncodedMessage = 1):

        encodedImage = image;

        stegUtils = SteganographyUtils.SteganographyUtils()
        binaryMessage = stegUtils.GetBinaryMessageString(message)    

        print("Size: "+ str((encodedImage.size/3)/numberOfSections))  
        xLength = np.size(encodedImage, 1)
        yLength = np.size(encodedImage, 0)
        print("x: "+str(xLength))        
        print("y: "+str(yLength))      

        step = encodedImage.size/3/numberOfSections
        counter = 0

        for colorIndex in range(3):
            while(counter < encodedImage.size/3):
                if(counter >= len(binaryMessage)):
                    if(counter == len(binaryMessage) and showEncodedMessage != 0):
                        self.PrintEncodingStart(message, colorIndex)
                    break;

                # EncodeByte
                n = step * counter - (colorIndex * step * numberOfSections)

                if(int(n) >= encodedImage.size/3):
                    # next color
                    print("Next color!")
                    break;
                    
                x = int(n)
                y = 0

                while(x>xLength):
                    y += 1
                    x -= xLength
                #print("x: "+str(x)+", y:" +str(y))
                                
                a = encodedImage[x-1, y,colorIndex].astype(int) 
                
                if(binaryMessage[counter]=='1'): a = a | 1                    
                else: a = a & ~1

                encodedImage[x-1, y,colorIndex] = a
                counter += 1

        if(counter < len(binaryMessage)):
            print("Warning: Message is not fully encoded. Bytes encoded: "+ str(counter/8))  

        return encodedImage


