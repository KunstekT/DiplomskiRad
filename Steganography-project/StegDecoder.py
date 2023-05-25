import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

class StegDecoder:

    def ImageToBinaryMessage(self, image):
        hiddenBinaryMessage = ""
        
        counter = -1
        xy = np.shape(image)
        imageSize=xy[0]*xy[1]
        for color in range(3):
            for i in range(np.size(image, 0)):
                for j in range(np.size(image, 1)):
                    counter+=1
                    #print("Pixel(R)", counter, "(", image[i][j],")")
                    num = (image[i][j])[color]%2
                    num = num.item()
                    hiddenBinaryMessage += str(num)
        return hiddenBinaryMessage

    def BinaryMessageToString(self, hiddenBinaryMessage):
        hiddenMessage = ""
        binaryChar = ""
        counter = -1
        for n in hiddenBinaryMessage:
            counter += 1
            if(counter == 7):
                binaryChar = binaryChar + n 

                if(int(binaryChar, 2)>31):
                    hiddenMessage += chr(int(binaryChar, 2))

                binaryChar=""
                counter = -1
            else:
                binaryChar = binaryChar + n   
        return hiddenMessage

    def RemoveAfterStopSign(self, hiddenMessage, stopSign):
        old = hiddenMessage
        hiddenMessage = ""
        for c in old:
            if(ord(c)==ord(stopSign)):
                break;
            else:
                hiddenMessage = hiddenMessage + c
        return hiddenMessage

    def FilterNonRegularCharacters(self):
        old = hiddenMessage
        hiddenMessage = ""
        for c in old:
            if(ord(c)<32 or ord(c)>127):
                break;
            else:
                hiddenMessage = hiddenMessage + c
        return hiddenMessage

    def ShowDecodedMessage(self, message):        
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~ Steganography Decoder ~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Decoded message: ")
        print(message)  
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 
        
        # messageFilter: if true: filters characters that do not belong between 32 and 127 ASCII values (inclusive)
    def Decode(self, image, messageFilter = False, showMessage = False, showImage = False, decodeUntilStopSign=False, stopSign='$'):    
        
        if(showImage):
            plt.figure()
            plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
            #plt.show()
            
        hiddenBinaryMessage = self.ImageToBinaryMessage(image)
        hiddenMessage = self.BinaryMessageToString(hiddenBinaryMessage)                       
                
        if(decodeUntilStopSign==True):
            hiddenMessage = self.RemoveAfterStopSign(hiddenMessage, stopSign)

        if(messageFilter == True):
            hiddenMessage = self.FilterNonRegularCharacters(hiddenMessage)

        if(showMessage):
            self.ShowDecodedMessage(hiddenMessage)

        return hiddenMessage