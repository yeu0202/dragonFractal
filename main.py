import cv2
import numpy as np
import time
import math
import imutils



# time calculation
start_time = time.time()
fpsDisplayTime = 1  # displays the frame rate every 1 second
fpsCounter = 0


# font variables
font = cv2.FONT_HERSHEY_SIMPLEX
fontOrigin = (10, 35)
fontScale = 1
fontColour = (255, 255, 255)
fontBorderColour = (0, 0, 0)
fontThickness = 2

def myPutText(img, text):
    outputImage = cv2.putText(img, text, fontOrigin, font, fontScale, fontBorderColour, fontThickness+3, cv2.LINE_AA)
    outputImage = cv2.putText(outputImage, text, fontOrigin, font, fontScale, fontColour, fontThickness, cv2.LINE_AA)
    return outputImage


# stack images for display
def myStackImages(scale, imgArray):
    outputImage = None
    for i in range(len(imgArray)):
        rowStack = np.hstack(imgArray[i])
        if outputImage is not None:
            outputImage = np.vstack((outputImage, rowStack))
        else:
            outputImage = rowStack

    outputImage = cv2.resize(outputImage, (round(outputImage.shape[1]*scale), round(outputImage.shape[0]*scale)))
    return outputImage


imgHeight = 1000
imgWidth = 1000

img = np.zeros((imgHeight, imgWidth, 3), np.uint8)
cv2.imshow('Video', img)


linesArray = []

class MyLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def draw(self, outerImg):
        outerImg = cv2.line(outerImg, (self.x1, self.y1), (self.x2, self.y2), (255, 255, 0), 1)

    def split(self, outputArray):
        x3 = (self.x2 + self.x1) / 2 - (self.y2 - self.y1) / 2
        y3 = (self.y2 + self.y1) / 2 + (self.x2 - self.x1) / 2

        line1 = MyLine(self.x1, self.y1, x3, y3)
        line2 = MyLine(self.x2, self.y2, x3, y3)
        outputArray.append(line1)
        outputArray.append(line2)

firstLine = MyLine(300, 500, 800, 500)
linesArray.append(firstLine)
linesArray[0].draw(img)
cv2.imshow('Video', img)
time.sleep(3)

iterations = 0

while True:
    time.sleep(1)

    # don't know how to find the next rotate coordinate
    # img2 = img.copy()
    #
    # img = imutils.rotate(img, 45)
    # img2 = imutils.rotate(img2, -45)
    #

    img = np.zeros((imgHeight, imgWidth, 3), np.uint8)
    for lines in linesArray:
        lines.draw(img)

    tempArray = []
    for lines in linesArray:
        lines.split(tempArray)

    linesArray = tempArray


    # Display the resulting frame
    cv2.imshow('Video', img)

    if cv2.waitKey(1) & 0xFF == ord('q') or iterations == 19:
        time.sleep(5)
        break

    iterations = iterations + 1

