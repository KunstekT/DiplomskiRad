from uu import encode
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

import SteganographyUtils
import StegEncoder
import StegDecoder
import StegSectionsEncoder
import StegSectionsDecoder
import StegPatchEncoder
import StegPatchDecoder
import StegCannyPatchEncoder
import Steganalyzer

stegUtils = SteganographyUtils.SteganographyUtils()
encoder = StegEncoder.StegEncoder()
decoder = StegDecoder.StegDecoder()
encoderSect = StegSectionsEncoder.StegSectionsEncoder()
decoderSect = StegSectionsDecoder.StegSectionsDecoder()
encoderPatch = StegPatchEncoder.StegPatchEncoder()
decoderPatch = StegPatchDecoder.StegPatchDecoder()
encoderCannyPatch = StegCannyPatchEncoder.StegCannyPatchEncoder()
# decoderCannyPatch
steganalyzer = Steganalyzer.Steganalyzer()

#messageToEncode = "Lorem ipsum"
#messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras nunc quam, scelerisque sed ex sit amet, laoreet tincidunt lacus. Vivamus aliquet elit vitae pretium semper. Sed faucibus quam maximus sapien convallis volutpat. Cras consectetur mi vel lacus elementum efficitur. Cras pharetra nibh sit amet neque varius sollicitudin. Nulla aliquet eros a mi tincidunt tempor. Etiam quis nisi iaculis, venenatis tellus ac, fringilla urna. Duis condimentum dui et diam vulputate tincidunt. Nulla quis nulla ut elit bibendum suscipit. Nam nisi sem, sodales at elementum eget, consequat in tellus. Nam ante urna, tincidunt id malesuada ut, porttitor ac purus. Cras consequat ipsum sed enim euismod, vitae tempor mauris aliquet. Curabitur commodo malesuada ornare. Curabitur eget nibh tellus. Curabitur vitae nulla lacinia urna pharetra blandit at non tortor. Fusce a tellus eu ante euismod convallis in eget nulla. Donec tortor nulla, cursus cursus sagittis non, semper sed neque. Ut pretium ante id imperdiet consectetur. Pellentesque tempus turpis sit amet risus fermentum maximus. Proin id hendrerit nulla. Praesent finibus, libero id efficitur ultricies, velit diam dapibus purus, a suscipit mi urna a lorem. Aenean vulputate facilisis arcu, a volutpat mauris rhoncus eget. Aliquam quis mollis risus, ut consequat elit. Morbi aliquet velit sagittis aliquet porttitor. Donec vel arcu ut elit lacinia varius. Aliquam justo est, finibus non erat a, lacinia feugiat ligula. Nulla lacinia faucibus enim sed pharetra. Maecenas quam leo, convallis sit amet lectus at, cursus ornare sapien. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean ut mauris semper, porta tellus a, ultrices urna. In ac risus dolor. Donec interdum rhoncus velit nec elementum. Sed ut congue augue. Aliquam erat volutpat. Pellentesque at velit sit amet est iaculis pharetra. Aliquam pellentesque vestibulum varius. Vivamus commodo diam leo, quis eleifend eros bibendum et. Nam semper nibh eu posuere faucibus. Curabitur condimentum vitae nunc non faucibus. Nullam accumsan et nulla a eleifend. Ut ligula est, pellentesque quis est vel, dictum molestie urna. Aenean id elit in ante fermentum ornare. Cras accumsan leo eget velit blandit, vel aliquam nisl tincidunt. Morbi venenatis velit in neque iaculis, at posuere arcu dapibus. Aenean pellentesque ullamcorper eros vel elementum. Nullam justo quam, hendrerit ut vehicula vel, malesuada scelerisque lectus. In sed purus at tellus rutrum hendrerit. In eget vehicula dui. Sed in ante et turpis interdum ultrices. In ex velit, cursus non est quis, aliquam ultricies massa. Sed fringilla sed libero dapibus pharetra. Fusce in orci vitae augue ultrices auctor malesuada a quam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent pulvinar sed velit non hendrerit. Pellentesque aliquet sagittis sem, ut pharetra sem tempus id. Proin ut quam pharetra, malesuada ante eu, interdum nisl. Aliquam lobortis in odio ac efficitur. Cras rutrum leo non enim pretium, eget porttitor libero tincidunt. Mauris arcu lectus, semper sit amet justo eget, tempor egestas arcu."
for i in range(5):
    messageToEncode = messageToEncode + messageToEncode
    
image = cv.imread("images/lenna.png", cv.IMREAD_COLOR)
encoded_image = encoder.GetEncodedImage(image, messageToEncode)
msg = decoder.Decode(encoded_image, messageFilter=True)
print("Decoded message: "+msg)

print("------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------")

step = 8
encoded_patches_image = encoderPatch.GetEncodedImage(messageToEncode, image, step, addStopSigns= True)
pmsg = decoderPatch.Decode(encoded_patches_image, step, decodeUntilStopSign=True)
print("Decoded message (patches): "+pmsg)

cv.imshow('Original Image', image)
cv.imshow('Encoded Image', encoded_image)
cv.imshow('Encoded Image (in patches)', encoded_patches_image)
cv.waitKey(0) 

cv.imwrite('images/output/encoded_image.jpg', encoded_image)
cv.imwrite('images/output/encoded_patches_image.jpg', encoded_patches_image)

print("------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------")
print("")
print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Steganalyzer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("  -- Sequential LSB encoding")

resultR, resultG, resultB = steganalyzer.Analyze(encoded_image, 1000)
print(" Probability of hidden message in the red channel: {:.2f}%".format(resultR*100))
print(" Probability of hidden message in the green channel: {:.2f}%".format(resultG*100))
print(" Probability of hidden message in the blue channel: {:.2f}%".format(resultB*100))        
print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

print("  -- Patch encoding ("+str(step)+"x"+str(step)+")")
resultR, resultG, resultB = steganalyzer.Analyze(encoded_patches_image, 1000)
print(" Probability of hidden message in the red channel: {:.2f}%".format(resultR*100))
print(" Probability of hidden message in the green channel: {:.2f}%".format(resultG*100))
print(" Probability of hidden message in the blue channel: {:.2f}%".format(resultB*100))        
print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

histogram_R, bin_edges_R = steganalyzer.getHistogram(encoded_image, 0)
e_R, OddIndexes_R = steganalyzer.GetImageChannelFeatures(encoded_image, 0)

P_histogram_R, P_bin_edges_R = steganalyzer.getHistogram(encoded_patches_image, 0)
P_e_R, P_OddIndexes_R = steganalyzer.GetImageChannelFeatures(encoded_patches_image, 0)

stegUtils.CompareHistograms(histogram_R, P_histogram_R, bin_edges_R, P_bin_edges_R, "Histogram comparision", "Sequential LSB method","Patch LSB method")
