# import delle librerie
import argparse
import datetime
import time
import imutils
import cv2

# parser degli argomenti da linea di comando, come funziona?
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

vs = cv2.VideoCapture(0)

# inizializzare il primo frame
firstFrame = None

# loop su tutti i frame del video
while True:
	# cattura del frame corrente
	_, frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied"

	# se il frame è vuoto allora si è alla fine del video
	if frame is None:
		break

	# resize del frame, conversione a scala di grigi e succesiva sfocatura
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# se il primo frame è None, viene inizializzato
	if firstFrame is None:
		firstFrame = gray
		continue
    # calcolo della differenza assoluta tra il primo frame e quello corrente
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilata l'immagine a cui viene applicata la soglia, poi trova i contorni
	#thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop sui contorni
	for c in cnts:
		# i contorni troppo piccoli sono ingnorati
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# calcola il rettangolo che delimita il contorno, lo disegna e fa l'update del testo
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

    # disegna testo e ora sull'immagine
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# mostra le immagini
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# il tasto q blocca il loop
	if key == ord("q"):
		break

# chiude le finestre
cv2.destroyAllWindows()