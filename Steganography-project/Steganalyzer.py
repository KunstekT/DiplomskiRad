import numpy as np
import cv2 as cv
import scipy as sp
import matplotlib.pyplot as plt

class Steganalyzer(object):

    def LoadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)

        # Used to load unmodified image, one used to compare with modified
    def loadUnmodifiedImage(self, link):
        self.unmodifiedImage = cv.imread(link, cv.IMREAD_COLOR)

    # Unused
    def getHistogram(self, image, color_channel_id):
        plt.xlim([0, 256])
        histogram, bin_edges = np.histogram(image[:, :, color_channel_id], bins=256, range=(0, 256))
        return histogram, bin_edges

    def showHistogram(self, histogram, bin_edges, color):
        #plt.figure()
        plt.plot(bin_edges[0:-1], histogram, color)
        #print(histogram)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram, color channel: " + color)

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

        # ? Prints out comparison of values needed for chi test
    def printComparisionTable(self, OddIndexAverages, e, OddIndexAverages2, e2):
        blankimage = np.zeros([100,100,3],dtype=np.uint8)
        blankimage.fill(0) # or img[:] = 255
        if(self.unmodifiedImageLink != ""):
            print("________________________________________")
            print("original image is loaded for comparision")
            print("____|edited image   |   original image")
            for i in range(len(e)):
                print("["+ str(i) +"]: Odd: "+ str(OddIndexAverages[i]) +", e: "+  str(e[i]) + "   |   Odd: "+ str(OddIndexAverages2[i]) +", e: "+  str(e2[i]) + " ")
        else:
            for i in range(len(e)):
                print("["+ str(i) +"]: Odd: "+ str(OddIndexAverages[i]) +", e: "+  str(e[i]))
    
    # Unused
    def getHistogramPairValues(self, histogram):
        histogram_pair_values = []
        for i in range(1, 256, 2):
            pair_value = [histogram[i-1], histogram[i]]
            histogram_pair_values.append(np.array(pair_value))
        return histogram_pair_values

    # Unused
    def getPairValuesAverages(self, values):
        PairValuesAverages = list()
        i = 0
        avg = 0
        for i in range(len(values)-1):
            if(i%2==0):
                avg=(values[i]+values[i+1])/2
                PairValuesAverages.append(avg)
        return PairValuesAverages

    def GetImageChannelFeatures(self, image, colorId):
        if(colorId < 0 or colorId > 2):
            colorId = 0
        histogramData, bin_edges = np.histogram(image[:, :, colorId], bins=256, range=(0, 256))
        averagedPairs = [(histogramData[i] + histogramData[i+1]) / 2 for i in range(0, len(histogramData)-1, 2)]
        oddIndexElements = histogramData[1::2]
        return averagedPairs, oddIndexElements
    
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
        x = (expValues/exp_sum)*obs_sum
        chi, p = sp.stats.chisquare(obsValues, x, 0)           
        return p

    def PrintHistogramValues(self, histogram, e, OddIndexes):
        print("\n--------------------------")
        print("\n- histogram -----------")
        print(histogram[:])
        print("\n- e -----------")
        print(e[:])
        print("\n- OddIndexes -----------")
        print(OddIndexes[:])
        print("--------------------------")
 
# ...  # self.PrintHistogramValues(histogram_R, e0, OddIndexes_R)

    def Analyze(self, image, nRowsToCheck):
        if(nRowsToCheck>image.shape[1]):
            nRowsToCheck = image.shape[1]
        print(" Analyzing", nRowsToCheck, "rows (", nRowsToCheck/image.shape[1]*100, "%)")
        imagePartToCheck = image[0:nRowsToCheck,:,:]

        e_R, oddIndexElements_R = self.GetImageChannelFeatures(imagePartToCheck, 0)        
        resultR = self.ChiSquareTest(oddIndexElements_R, e_R)
        e_G, oddIndexElements_G = self.GetImageChannelFeatures(imagePartToCheck, 1)
        resultG = self.ChiSquareTest(oddIndexElements_G, e_G)
        e_B, oddIndexElements_B = self.GetImageChannelFeatures(imagePartToCheck, 2)
        resultB = self.ChiSquareTest(oddIndexElements_B, e_B)

        return resultR, resultG, resultB



