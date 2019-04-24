import RPi.GPIO as GPIO
import cv2
import numpy as np
import time
from AlphaBot import AlphaBot

Ab = AlphaBot()

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
widthScreen= 320           
heightScreen= 200

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,widthScreen)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,heightScreen)

font=cv2.FONT_HERSHEY_SIMPLEX
kernel = np.ones((5,5),np.uint8)

def nothing(x):
    pass

# Creating a windows for later use
cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('tracking')


# Creating track bar for min and max for hue, saturation and value
# You can adjust the defaults as you like
cv2.createTrackbar('hmin', 'HueComp',12,179,nothing)
cv2.createTrackbar('hmax', 'HueComp',37,179,nothing)

cv2.createTrackbar('smin', 'SatComp',96,255,nothing)
cv2.createTrackbar('smax', 'SatComp',255,255,nothing)

cv2.createTrackbar('vmin', 'ValComp',186,255,nothing)
cv2.createTrackbar('vmax', 'ValComp',255,255,nothing)




while True:
    # SENSORI IR
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
        
    #PICAM
    _, frame = video.read()
    frame=cv2.resize(frame,(widthScreen,heightScreen))   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)

    # get info from track bar and appy to result
    hmn = cv2.getTrackbarPos('hmin','HueComp')
    hmx = cv2.getTrackbarPos('hmax','HueComp')
    

    smn = cv2.getTrackbarPos('smin','SatComp')
    smx = cv2.getTrackbarPos('smax','SatComp')


    vmn = cv2.getTrackbarPos('vmin','ValComp')
    vmx = cv2.getTrackbarPos('vmax','ValComp')

    # Apply thresholding
    hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
    sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
    vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

    # AND h s and v
    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))

    # Some morpholigical filtering
    dilation = cv2.dilate(tracking,kernel,iterations = 1)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.GaussianBlur(closing,(5,5),0)

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=10,maxRadius=0)
    # circles = np.uint16(np.around(circles))
    
    circlePresent = False
    if circles is not None:
        circlePresent = True
        for i in circles[0,:]:
            cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
            cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
            xcenter = int(round(i[0]))
            ycenter = int(round(i[1]))
    if circlePresent:
        print("Circle: "+ str(xcenter) + ', ' +str(ycenter))
    if ((DL_status == 1) and (DR_status == 1)) and (circlePresent == True) and (xcenter > widthScreen/3.*2.):
        Ab.right()
        print("Going right - right circle found "+ str(xcenter) + ', ' +str(ycenter))
    elif ((DL_status == 1) and (DR_status == 1)) and (circlePresent == True) and (xcenter < widthScreen/3.):
        Ab.left()
        print("Going left - left circle found")
    elif ((DL_status == 1) and (DR_status == 1)) and (circlePresent == True) and (xcenter >= widthScreen/3.) and (xcenter <= widthScreen/3.*2.):
        Ab.left()
        print("Going forward - front circle found")
    else:
        Ab.stop()
        print("Stop")

    cv2.imshow('HueComp',hthresh)
    cv2.imshow('SatComp',sthresh)
    cv2.imshow('ValComp',vthresh)
    cv2.imshow('closing',closing)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF #controllo di pressione del tasto ESC
    if k == 27:
        break

GPIO.cleanup()
cv2.destroyAllWindows()

