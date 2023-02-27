import numpy as np
import cv2 as cv

class StegSectionsDecoder:

        # messageFilter: if true: filters characters that do not belong between 32 and 127 ASCII values (inclusive)
    def Decode(self, image, messageFilter = True):    

        hiddenBinaryMessage = ""
        
        counter = -1
        xy = np.shape(image)
        imageSize=xy[0]*xy[1]
        for color in range(3):
            for i in range(np.size(image, 0)):
                for j in range(np.size(image, 1)):
                    counter+=1
                    if(color == 0):
                        #print("Pixel(R)", counter, "(", image[i][j],")")
                        num = (image[i][j])[0]%2
                        num = num.item()
                        hiddenBinaryMessage += str(num)
                    if(color == 1):
                        #print("Pixel(G)", counter-imageSize, "(", image[i][j],")")                                                
                        num = (image[i][j])[1]%2
                        num = num.item()
                        hiddenBinaryMessage += str(num)
                    if(color == 2):      
                        #print("Pixel(B)", counter-imageSize*2, "(", image[i][j],")")                                                
                        num = (image[i][j])[2]%2
                        num = num.item()
                        hiddenBinaryMessage += str(num)

        #print("")                
        #print("Decoded message (binary): ", hiddenBinaryMessage)
        #print("")  

        hiddenMessage = ""
        binaryChar = ""
        counter = -1
        for n in hiddenBinaryMessage:
            counter += 1
            if(counter == 7):
                binaryChar = binaryChar + n 

                #print(binaryChar + " " + str(int(binaryChar, 2)) + " " + chr(int(binaryChar, 2)))

                if(int(binaryChar, 2)>31):
                    hiddenMessage += chr(int(binaryChar, 2))

                binaryChar=""
                counter = -1
            else:
                binaryChar = binaryChar + n     
        
        if(messageFilter != 0):
            old = hiddenMessage
            hiddenMessage = ""
            for c in old:
                if(ord(c)<32 or ord(c)>127):
                    break;
                else:
                    hiddenMessage = hiddenMessage + c
        print("\n~~~~~~~~~~~~~~~~~~~~ Steganography Sections Decoder ~~~~~~~~~~~~~~~~~~~~")
        print("Decoded message: ")
        print(hiddenMessage)  
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 
