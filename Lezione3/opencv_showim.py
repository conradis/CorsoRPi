#import OpenCV
import cv2 

#associazione alla camera /dev/video0
cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read() #cattura di un frame
    cv2.imshow('frame',frame) #disegno a schermo del frame

    k = cv2.waitKey(5) & 0xFF #controllo di pressione del tasto ESC
    if k == 27:
        break

#chiusura della finestra
cv2.destroyAllWindows()
