import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

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

    def getHistogram(self, image, color_channel_id):
        plt.xlim([0, 256])
        histogram, bin_edges = np.histogram(image[:, :, color_channel_id], bins=256, range=(0, 256))
        return histogram, bin_edges

    def getHistogramPairValues(self, histogram):
        pairvalue=list()
        histogramPairValues = list()
        i=1
        for i in range(256):
            pairvalue.clear()
            if(i%2==1):
                pairvalue.append(histogram[i-1])
                pairvalue.append(histogram[i])
                vectorpairvalue = np.array(pairvalue)
                histogramPairValues.append(vectorpairvalue)
        return histogramPairValues

    def getPairValuesAverages(self, values):
        PairValuesAverages = list()
        i = 0
        avg = 0
        for i in range(len(values)-1):
            if(i%2==0):
                avg=(values[i]+values[i+1])/2
                PairValuesAverages.append(avg)
        return PairValuesAverages

    def getOddIndexElements(self, elements):
        oddIndexElements = []
        i=0
        for i in range(len(elements)):
            if(i%2==1):
                oddIndexElements.append(elements[i])
        return oddIndexElements

    def GetImageChannelFeatures(self, values, color):
        c=0
        if(color == 0 or color == 1 or color == 2):
            c=color
        else:
            print("Warning: wrong color channel input, channel 0 taken (function: GetImageChannelFeatures)")

        histogramData, bin_edges = self.getHistogram(values, c)
        histogramPairValues = self.getHistogramPairValues(histogramData)
        e = self.getPairValuesAverages(histogramData)
        oddIndexes = self.getOddIndexElements(histogramData)

        return histogramData, bin_edges, histogramPairValues, e, oddIndexes
    

    def showHistogram(self, histogram, bin_edges, color):
        #plt.figure()
        plt.plot(bin_edges[0:-1], histogram, color)
        #print(histogram)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram of \"" + self.imageLink + "\", color channel: " + color)

    def compareHistograms(self, histogram1, histogram2, bin_edges1, bin_edges2, color1, color2):
        #plt.figure()
        plt.plot(bin_edges1[0:-1], histogram1, color1)
        plt.plot(bin_edges2[0:-1], histogram2, color2)
        #print(histogram)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram comparision")
        plt.legend(['lenna.png', 'beach_indexed.png'])
        #plt.legend(['Unedited image', 'Edited image'])

    def GetSumsAndValues(self, inObserved, inExpected):        
        observed = []
        expected = []

        for x in range(len(inExpected)-1):
            observed.append(inObserved[x])
            expected.append(inExpected[x])

        for x in reversed(range(len(inExpected)-1)):
            if(inExpected[x] == 0):
                observed.pop(x)
                expected.pop(x)

        exp_sum = sum(expected)
        obs_sum = sum(observed)

        return obs_sum, exp_sum, observed, expected     

    def ChiSquareTest(self, observed, expected):
        obs_sum, exp_sum, obsValues, expValues = self.GetSumsAndValues(observed, expected)
        exp2 = (expValues/exp_sum)*obs_sum
        chi, p = sp.stats.chisquare(obsValues, exp2, 0)           
        return p
    
    def GetPositionsList(self, values):
        positions_list=[]
        for i in range(len(values)):
            x = int(int(values[i])/8)
            positions_list.append(x)
        return positions_list

    def AddStopSignsToMessage(self, message, positions, stopSign="$"):        
        positions_list = self.GetPositionsList(positions)     
        
        ogPositions = positions_list
        for i in range(len(positions_list)):
            if(positions_list[i] - 1 < 0):
                pass            
            else:
                positions_list[i] = positions_list[i]-1
            #if(positions_list[i] == 0):
            #    positions_list[i] = 1

        positions_list = np.cumsum(positions_list)
        for i in range(len(positions_list)):
            positions_list[i] = positions_list[i] + i

        #print("Cumulative (positions in string after '$' addition): ",positions[:20])

        x = 0;
        for pos in positions_list:

            if(x == pos):
                message = message[:pos] + stopSign + message[pos:]
                continue
            else:
                x = pos
                
            message = message[:pos] + stopSign + message[pos:]
            pos += 1  # Increase the position by 1 after inserting '$'
            
        print("------------------------------------------------------------------------------")
        print("positions: ",ogPositions[:80],"...") 
        print(">>>result: ",message[:50],"...")
        print("------------------------------------------------------------------------------")
        return message



