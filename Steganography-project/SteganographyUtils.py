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
        stringList = []
        characters = []
        for i in message:
            x=ord(i)
            characters.append(x)
        for i in characters:
            s = "{:08b}".format(i)
            stringList.append(s)
        return ''.join(stringList)         

    def PrintByte(self, a):
        print(format(a, '0{}b'.format(8)))       

    def GetByteRepresentation(self, a):
        return format(a, '0{}b'.format(8))

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
        plt.plot(bin_edges[0:-1], histogram, color)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram of \"" + self.imageLink + "\", color channel: " + color)

    def PlotCompareHistograms(self, histogram1, histogram2, bin_edges1, bin_edges2):
        plt.hist(histogram1, bins=bin_edges1, label='Histogram 1')
        plt.hist(histogram2, bins=bin_edges2, label='Histogram 2')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.legend()        
        plt.show()

    def CompareHistograms(self, histogram1, histogram2, bin_edges1, bin_edges2, title, name1, name2):
        plt.plot(bin_edges1[0:-1], histogram1)
        plt.plot(bin_edges2[0:-1], histogram2)
        plt.xlabel("Color values")
        plt.ylabel("Frequency")
        plt.title(title)
        plt.legend([name1, name2])
        plt.show()    
        
    def CompareThreeHistograms(self, histogram1, histogram2, histogram3, bin_edges1, bin_edges2, bin_edges3, title, name1, name2, name3):
        plt.plot(bin_edges1[0:-1], histogram1)
        plt.plot(bin_edges2[0:-1], histogram2)
        plt.plot(bin_edges3[0:-1], histogram3)
        plt.xlabel("Color values")
        plt.ylabel("Frequency")
        plt.title(title)
        plt.legend([name1, name2, name3])
        plt.show()

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

    def AddStopSignsToMessage(self, message, dataAmounts, stopSign="$"):       
        data = []
        for i in range(len(dataAmounts)):
            x = int(int(dataAmounts[i])/8)
            data.append(x)
        for i in range(len(data)):
            if(data[i] - 1 >= 0):
                data[i] = data[i]-1
        data = np.cumsum(data)
        for i in range(len(data)):
            data[i] = data[i] + i
        for position in data:
            message = message[:position] + stopSign + message[position:]               
        return message
