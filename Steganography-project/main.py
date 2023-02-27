import numpy as np
import cv2 as cv
import StegEncoder
import StegDecoder
import StegSectionsEncoder
import StegSectionsDecoder
import Steganalyzer

messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

image = cv.imread("images/beach_indexed.png", cv.IMREAD_COLOR)

encoder = StegEncoder.StegEncoder()
decoder = StegDecoder.StegDecoder()
encoderSect = StegSectionsEncoder.StegSectionsEncoder()
decoderSect = StegSectionsDecoder.StegSectionsDecoder()
steganalyzer = Steganalyzer.Steganalyzer()

encodedImage = encoder.GetEncodedImage(image, messageToEncode)
decoder.Decode(encodedImage, True)

encodedImageSect = encoderSect.GetEncodedImage(image, messageToEncode)
decoderSect.Decode(encodedImageSect, True)

steganalyzer.Analyze(encodedImage, 1)
steganalyzer.Analyze(encodedImageSect, 1)