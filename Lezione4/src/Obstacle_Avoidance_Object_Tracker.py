import RPi.GPIO as GPIO
import cv2
import numpy as np
import time
from AlphaBot import AlphaBot

def findObject(frame):
    """
    La funzione legge in input un frame letto tramite VideoCapture
    e individua gli oggetti rossi presenti nell'immagine.
    La funzione ritorna una tupla contenente:
    - objPresent: bool che indica se almeno un oggetto e presente
    - xcenter: coordinata x del centro dell'oggetto
    - ycenter: coordinata y del centro dell'oggetto
    - frame: il frame contenente un rettangolo che evidenzia l'oggetto rilevato
    """
    font=cv2.FONT_HERSHEY_SIMPLEX
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))

    lower_red_0 = np.array([0, 100, 100]) 
    upper_red_0 = np.array([10, 255, 255])
    lower_red_1 = np.array([180 - 10, 100, 100]) 
    upper_red_1 = np.array([180, 255, 255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask_0 = cv2.inRange(hsv, lower_red_0 , upper_red_0)        
    mask_1 = cv2.inRange(hsv, lower_red_1 , upper_red_1 )

    mask = cv2.bitwise_or(mask_0, mask_1)

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    
    im,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 
    cv2.drawContours(frame,conts,-1,(255,0,0),3)
    objPresent = False 
    xcenter = -1
    ycenter = -1
    
    if len(conts) > 0:
        x,y,w,h=cv2.boundingRect(conts[0])
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2) 
        xcenter=x+w/2
        ycenter=y+h/2
        cv2.putText(frame, str(int(xcenter))+','+str(int(ycenter)),(x,y+h),font,.5,(0,255,255))
        objPresent = True 
    return objPresent, xcenter, ycenter, frame

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
video.set(3,widthScreen)
video.set(4,heightScreen)


while True:
    # SENSORI IR
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
        
    #PICAM
    _, frame = video.read()
    objPresent, xcenter, ycenter, frame = findObject(frame)

    if((DL_status == 1) and (DR_status == 1)) and (objPresent == False):
        Ab.forward()
        print("Going forward - no object found")
    elif ((DL_status == 1) and (DR_status == 1)) and (objPresent == True) and (xcenter > widthScreen/2):
        Ab.right()
        print("Going right - right object found")
    elif ((DL_status == 1) and (DR_status == 1)) and (objPresent == True) and (xcenter <= widthScreen/2):
        Ab.left()
        print("Going left - left object found")
    elif((DL_status == 1) and (DR_status == 0)):
        Ab.left()
        print("Going left - right obstacle")
    elif((DL_status == 0) and (DR_status == 1)):
        Ab.right()
        print("Going right - left obstacle")
    else:
        Ab.backward()
        time.sleep(0.2)
        Ab.left()
        time.sleep(0.2)
        Ab.stop()
        print("backward")
        
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF #controllo di pressione del tasto ESC
    if k == 27:
        break

GPIO.cleanup()
cv2.destroyAllWindows()

