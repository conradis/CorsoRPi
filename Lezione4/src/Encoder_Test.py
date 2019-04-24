import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot

Ab = AlphaBot()
Ab.stop()

ENCR = 8
ENCL = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ENCL,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(ENCR,GPIO.IN,GPIO.PUD_UP)

ENCR_status = 0
ENCL_status = 0
ENCR_counter = 0
ENCL_counter = 0
try:
    while True:
        ENCR_status_new = GPIO.input(ENCR)
        ENCL_status_new = GPIO.input(ENCL)
        if ENCR_status_new != ENCR_status:
            ENCR_counter = ENCR_counter + 1
        ENCR_status = ENCR_status_new
        if ENCL_status_new != ENCL_status:
            ENCL_counter = ENCL_counter + 1
        ENCL_status = ENCL_status_new
        
        print (ENCR_counter,ENCL_counter)
        
except KeyboardInterrupt:
    GPIO.cleanup()
        
    