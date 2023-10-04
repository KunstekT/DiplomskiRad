import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

class SteganographyUtils:

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
    
    def showHistogram(self, histogram, bin_edges, color):
        plt.plot(bin_edges[0:-1], histogram, color)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram of \"" + self.imageLink + "\", color channel: " + color)

    def CompareHistograms(self, histogram1, histogram2, bin_edges1, bin_edges2, title, name1, name2):
        plt.plot(bin_edges1[0:-1], histogram1, color="green")
        plt.plot(bin_edges2[0:-1], histogram2, color="orange")
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
