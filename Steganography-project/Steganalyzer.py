import numpy as np
import cv2 as cv
import scipy as sp
import matplotlib.pyplot as plt

class Steganalyzer(object):

    def getHistogram(self, image, color_channel_id):
        plt.xlim([0, 256])
        histogram, bin_edges = np.histogram(image[:, :, color_channel_id], bins=256, range=(0, 256))
        return histogram, bin_edges

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



