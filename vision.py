from ctypes import sizeof
import cv2 as cv
import numpy as np
import math




#global varibles   

pi:float = 3.145

#values for isolating the red tomatos
low_green = np.array([12, 12, 25])
high_green = np.array([125, 255, 255])


#Read images
img = cv.imread('Images/multible.jpg')
#Resize
img = cv.resize(img, (900, 650), interpolation=cv.INTER_CUBIC)
#blur
img = cv.medianBlur(img,5)


    # convert BGR to HSV
imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # create the Mask
mask = cv.inRange(imgHSV, low_green, high_green)
    # inverse mask 
mask = 255-mask
res = cv.bitwise_and(img, img, mask=mask)

cv.imshow("input", img)
cv.waitKey()
cv.imshow("mask", mask)
cv.waitKey()
cv.imshow('Green removed', res)
cv.waitKey()


height, width, _ = res.shape
 
for i in range(height):
    for j in range(width):
        # img[i, j] is the RGB pixel at position (i, j)
        # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
        if res[i, j].sum() < 50:
            res[i, j] = [255, 255, 255]

cv.imshow("output", res)
cv.waitKey()

#convert to grayscale
grayImage = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
  
(thresh, blackAndWhiteImage) = cv.threshold(grayImage, 127, 255, cv.THRESH_BINARY)
 
cv.imshow('Black white image', blackAndWhiteImage)
cv.waitKey()

#circle detection
circles = cv.HoughCircles(blackAndWhiteImage,cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
cv.imshow('detected circles',img)
cv.waitKey(0)
