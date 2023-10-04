import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
import mouse
import numpy as np
import pyautogui


wCam = 440
hCam = 380
wScr = 1366
hScr = 768
frameR = 100
plocX = 0
plocY = 0
clocX = 0
clocY = 0
smoothening = 7

testx = 0
testy = 0
testxNorm = 0
testyNorm = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    cv2.rectangle(img, (100, 100), (340, 280), (255, 0, 0), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lista4 = []
            lista5 = []
            lista8 = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                if id == 4:
                    lista4.append(cx)
                    lista4.append(cy)
                if id == 5:
                    lista5.append(cx)
                    lista5.append(cy)
                if id == 8:
                    lista8.append(cx)
                    lista8.append(cy)
                    print(lista8[0], lista8[1])
                    if 340 > lista8[0] > 100 and 100 < lista8[1] < 280:

                        #print("Posicao Dedao ", lista4, "Posicao Indicador ", lista5)
                        testx = (lista4[0] - lista5[0]) ** 2
                        testy = (lista4[1] - lista5[1]) ** 2

                        testxNorm = math.sqrt(testx)
                        testyNorm = math.sqrt(testy)
                        cv2.circle(img, lista8, 15, (255, 0, 255), 3)
                        #moveX = lista8[0]
                        #moveY = lista8[1]
                        #print("Mouse position Movido para ", mouse.get_position())
                        x8 = np.interp(lista8[0], (frameR, wCam - frameR), (0, wScr))
                        y8 = np.interp(lista8[1], (frameR, hCam - frameR), (0, hScr))

                        clocX = plocX + (x8 - plocX) / smoothening
                        clocY = plocY + (y8 - plocY) / smoothening

                        mouse.move(wScr - clocX, clocY)
                        plocX, plocY = clocX, clocY

                        if testxNorm <= 5 and testyNorm <= 5:
                            #print("OK \nPosicao Dedao ", lista4, "Posicao Indicador ", lista5)
                            ok = "Click"
                            cv2.putText(img, str(ok), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 255), 3)
                            mouse.click()
                            print("Mouse position ", mouse.get_position())
                            print("X ", x8, "Lista x ", lista8[0])
                            print("Y ", y8, "Lista y ", lista8[1])

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Image", img)

    cv2.waitKey(1)
