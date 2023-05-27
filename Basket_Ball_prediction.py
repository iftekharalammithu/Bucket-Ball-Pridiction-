import cv2
import os
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
import math

## Load Video
video = cv2.VideoCapture("Videos/vid (4).mp4")
image = cv2.imread('Ball.png')



# Find The Ball Color
ball_color = ColorFinder(False)
color_code = {'hmin': 0, 'smin': 123, 'vmin': 0, 'hmax': 15, 'smax': 255, 'vmax': 255}

## Image Resize
image = image[0:900 , :]
image = cv2.resize(image, (int(image.shape[0]/1.5) , int(image.shape[1]/3)))

## Ball Position List
poslistx = []
poslisty = []


## image value
xlist = [ i for i in range(0,1300) ]

# Define the crop region
crop_x = 0
crop_y = 0
crop_width = 1300
crop_height = 950

# Get the video codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Set up the VideoWriter object
out = cv2.VideoWriter('result_vid_4.mp4', fourcc, 10.0, (crop_width, crop_height))

## Run Video
while video.isOpened():
    rat , cap = video.read()

    if rat == False:
        break

    ## Resize Video
    cap = cap[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]


    ## Find the ball Color
    color , mask = ball_color.update(cap , color_code)
    
    ## Find the Ball Location
    ballloc , location = cvzone.findContours(cap , mask, minArea=200)

    ## Append The Ball Center Location in List
    if location:
        poslistx.append(location[0]['center'][0])
        poslisty.append(location[0]['center'][1])

    if poslistx:
        ## Prediction of Ball
        a, b, c = np.polyfit(poslistx, poslisty, 2)

        ## Mark The Ball Position
        for i , (posx,posy) in enumerate(zip(poslistx,poslisty)):

            pos = (posx,posy)
            cv2.circle(ballloc, pos, 3, (0,150,0), cv2.FILLED)
            
            if i != 0:
                cv2.line(ballloc , pos, (poslistx[i-1] , poslisty[i -1]) , (200,0,0), 2)

        for x in xlist:
            y = int(a*x**2 + b*x + c)
            cv2.circle(ballloc, (x ,y), 1, (0,0,200), cv2.FILLED)

        ## Bucket value is x = 330 to 430 y = 590
        if len(poslistx) < 10:
            print(poslistx)
            c = c - 590
            x = int((-b - math.sqrt(b**2 - (4*a*c)))/ (2*a))
            position = 330<x<430

        ## Put Text Bucker or not
        if position:
            cvzone.putTextRect(ballloc,"Bucket" , (50 , 100) , scale=3 ,thickness= 2 , colorR=(0,200,0))
            print('bucker')
        else:
            cvzone.putTextRect(ballloc,"No Bucket" , (50 , 100) , scale=3 ,thickness= 2 , colorR=(0,0,200))



    ## Show Video/Image 
    cap = cv2.resize(ballloc, (int(cap.shape[0]/1.5) , int(cap.shape[1]/3)))
    cv2.imshow('color', cap)
    
    # Save The Output
    out.write(ballloc)
    
    
    # Exit on 'q' key press
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break