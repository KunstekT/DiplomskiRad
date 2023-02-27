import cv2 as cv

class SteganographyUtils:

    def LoadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)
        self.encodedImage = cv.imread(link, cv.IMREAD_COLOR)

    def SaveImage(self, link):     
        cv.imwrite(link, self.encodedImage)

    def ConvertMessageToBinary(self, message):
        stringList = list()
        characterList=[]
        for i in message:
            x=ord(i)
            characterList.append(x)
        for i in characterList:
            s = str(int(bin(i)[2:]))
            if(len(s)==7):
                s = "0" + s
            elif(len(s)==6):
                s = "00" + s
            elif(len(s)==5):
                s = "000" + s
            elif(len(s)==4):
                s = "0000" + s
            elif(len(s)==3):
                s = "00000" + s
            elif(len(s)==2):
                s = "000000" + s
            elif(len(s)==1):
                s = "0000000" + s
            else:
                s = "00000000"
            stringList.append(s)
        return stringList        

    def PrintByte(self, a):
        print(format(a, '0{}b'.format(8)))       

    def GetByteRepresentation(self, a):
        return format(a, '0{}b'.format(8))

    def GetBinaryMessageString(self, message):
        binaryMessageStringList = self.ConvertMessageToBinary(message)
        binaryMessageString=""
        for s in binaryMessageStringList:
            binaryMessageString+=s
        return binaryMessageString




