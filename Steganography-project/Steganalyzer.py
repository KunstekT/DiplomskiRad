import numpy as np
import cv2 as cv
import scipy as sp
import matplotlib.pyplot as plt

class Steganalyzer(object):

    #image = np.zeros([100,100,3],dtype=np.uint8)
    #image.fill(0)
    #imageLink = ""

    #unmodifiedImage = np.zeros([100,100,3],dtype=np.uint8)
    #unmodifiedImage.fill(0)
    #unmodifiedImageLink = ""

    def LoadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)

        # Used to load unmodified image, one used to compare with modified
    def loadUnmodifiedImage(self, link):
        self.unmodifiedImage = cv.imread(link, cv.IMREAD_COLOR)

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
            print("GetImageChannelFeatures warning: wrong color channel input, channel 0 taken")

        #print("\n\nGetImageChannelFeatures...color: ", color, ", ", c)  
        histogramData, bin_edges = self.getHistogram(values, c)
        histogramPairValues = self.getHistogramPairValues(histogramData)
        e = self.getPairValuesAverages(histogramData)
        OddIndexes = self.getOddIndexElements(histogramData)

        return histogramData, bin_edges, histogramPairValues, e, OddIndexes
    
    def ChiSquareTest(self, observed, expected):

        ## ↓ removing elements from arrays where 'expected' has zero ↓

        observed2 = []
        expected2 = []

        for x in range(len(expected)-1):
            observed2.append(observed[x])
            expected2.append(expected[x])

        for x in reversed(range(len(expected)-1)):
            if(expected[x] == 0):
                observed2.pop(x)
                expected2.pop(x)

        #print("Observed2 sum: ", np.sum(observed2))
        #print("Expected2 sum: ", np.sum(expected2))

        ## ↑ removing elements from arrays where 'expected' has zero ↑
        ## ↓ equalizing sums of expected and observed ↓

        exp_sum = sum(expected2)
        obs_sum = sum(observed2)

        exp2 = (expected2/exp_sum)*obs_sum
        #print("!! ", sum(exp2), "!!", sum(observed2))

        ## ↑ equalizing sums of expected and observed ↑

        chi, p = sp.stats.chisquare(observed2, exp2, 0)            
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
 
    def Analyze(self, image, nRowsToCheck):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Steganalyzer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if(nRowsToCheck>image.shape[1]):
            nRowsToCheck = image.shape[1]

        print("Number of image rows to analyze: ", nRowsToCheck, "[", nRowsToCheck/image.shape[1]*100, "%]")

        #image2 = np.zeros([100,100,3],dtype=np.uint8)
        image2 = image[0:nRowsToCheck,:,:]

        plt.figure()
        plt.imshow(cv.cvtColor(image2, cv.COLOR_BGR2RGB))
        plt.show()

        histogram_R, bin_edges_R, histogramPairValues_R, e_R, OddIndexes_R = self.GetImageChannelFeatures(image2, 0)
        #self.PrintHistogramValues(histogram_R, e0, OddIndexes0)
        result0 = self.ChiSquareTest(OddIndexes_R, e_R)

        self.showHistogram(histogram_R, bin_edges_R, "red")

        histogram_G, bin_edges_G, histogramPairValues_G, e_G, OddIndexes_G = self.GetImageChannelFeatures(image2, 1)
        #self.PrintHistogramValues(histogram_G, e1, OddIndexes1)
        result1 = self.ChiSquareTest(OddIndexes_G, e_G)

        histogram_B, bin_edges_B, histogramPairValues_B, e_B, OddIndexes_B = self.GetImageChannelFeatures(image2, 2)
        #self.PrintHistogramValues(histogram_B, e2, OddIndexes2)
        result2 = self.ChiSquareTest(OddIndexes_B, e_B)

        print("Probability of hidden message in the red channel: {:.2f}%".format(result0*100))
        print("Probability of hidden message in the green channel: {:.2f}%".format(result1*100))
        print("Probability of hidden message in the blue channel: {:.2f}%".format(result2*100))        
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

        plt.show()




