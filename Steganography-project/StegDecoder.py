import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

class StegDecoder:

    def ImageToBinaryMessage(self, image):
        hiddenBinaryMessage = ""        
        counter = -1
        for color in range(3):
            for i in range(np.size(image, 0)):
                for j in range(np.size(image, 1)):
                    counter+=1
                    num = (image[i][j])[color]%2
                    num = num.item()
                    hiddenBinaryMessage += str(num)
        return hiddenBinaryMessage

    def ImageToBinaryMessageFromChannel(self, image, channel):
        hiddenBinaryMessage = ""        
        counter = -1
        for i in range(np.size(image, 0)):
            for j in range(np.size(image, 1)):
                counter+=1
                num = (image[i][j])[channel]%2
                num = num.item()
                hiddenBinaryMessage += str(num)
        return hiddenBinaryMessage

    def ConvertBinaryToMessage(self, hiddenBinaryMessage):
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

    def FilterNonRegularCharacters(self, hiddenMessage):
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
    # decodeUntilStopSign: if true: stops decoding after the stop sign gets decoded
    # stopSign: '$' by default
    def Decode(self, image, messageFilter = False, decodeUntilStopSign=False, stopSign='$'):            
        hiddenBinaryMessage = self.ImageToBinaryMessage(image)
        hiddenMessage = self.ConvertBinaryToMessage(hiddenBinaryMessage)                       
                
        if(decodeUntilStopSign==True):
            hiddenMessage = self.RemoveAfterStopSign(hiddenMessage, stopSign)

        if(messageFilter == True):
            hiddenMessage = self.FilterNonRegularCharacters(hiddenMessage)

        return hiddenMessage

    def DecodeSingleChannel(self, image, channel, messageFilter = False, decodeUntilStopSign=False, stopSign='$'):
        hiddenBinaryMessage = self.ImageToBinaryMessageFromChannel(image, channel)
        hiddenMessage = self.ConvertBinaryToMessage(hiddenBinaryMessage) 

        if(decodeUntilStopSign==True):
            hiddenMessage = self.RemoveAfterStopSign(hiddenMessage, stopSign)

        if(messageFilter == True):
            hiddenMessage = self.FilterNonRegularCharacters(hiddenMessage)

        return hiddenMessage