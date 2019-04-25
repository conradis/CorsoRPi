import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot

Ab = AlphaBot()

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

try:
	while True:
		"""
            QUESTO E' IL LOOP PRINCIPALE DEL ROBOT
            Ad ogni ciclo si leggono i sensori e si controllano i motori.
            In questo loop si implementano gli algoritmi che implementano
            la logica del robot.
        """

except KeyboardInterrupt:
	GPIO.cleanup() #pulitura GPIO, onde evitare che i pin rimangano in stati spuri

