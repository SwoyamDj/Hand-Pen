import cv2
import mediapipe as mp
import time
import os
import htm
import numpy as np

choice="free"
mode="free"
prevx, prevy=0,0

mask = np.zeros((720,1280,3),np.uint8)


def recogniseGesture(li, li2):
    x=[li2[4][2],li2[3][2],li2[6][2],li2[10][2],li2[14][2],li2[18][2]]
    if li[1]==1 and li[2]==1:
            return "select"
    elif li[1]==1:
            return "draw"
    elif  x==sorted(x):
        return "thumbsup"
    else:
        return "free"


folder = "head"
l1 = os.listdir(folder)
l2=list()
for i in l1:
    img = cv2.imread(f'{folder}/{i}')
    l2.append(img)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while True:
    flag, img = cap.read()
    img = cv2.flip(img,1)

    #using htm
    detect = htm.handDetector(detectionCon=0.6)

    detect.findHands(img, draw=True)

    l3 = detect.findPosition(img, draw=False)
    # cv2.circle()

    if len(l3)!=0:
        # index finger
        xi, yi = int(l3[8][1] * 1280), int(l3[8][2] * 720)
        # middle finger
        x, y= xi, yi
        xm, ym = l3[8][1:]

    l4 = detect.fingersUp()
    if len(l4)!=0:
        mode=recogniseGesture(l4, l3)

    if mode=="select":
        prevx, prevy = 0, 0
        if ym<128:
            if 0< xm <200:
                choice="writer"
            elif xm <370:
                choice="line"
            elif 370< xm <555:
                choice="rectangle"
            elif 555< xm <740:
                choice="circle"
            else:
                choice="eraser"


        # working on choice


    if choice=="writer":
        try:
            xi, yi = l3[8][1:]
            # y9 = int(l3[9][2] * 720)

            if mode=="draw":
                if prevx !=0 and prevy!=0:
                    cv2.line(mask, (prevx, prevy), (xi, yi), (255,0,255), 4)
                    prevx, prevy = xi, yi

                else:
                    prevx = xi
                    prevy = yi
        except IndexError:
            continue
            
    if mode=="thumbsup":
        cv2.rectangle(mask, (0,128), (1280,720), (0,0,0), -1)

    print(choice, mode)

    imgrey = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    _, imginv = cv2.threshold(imgrey, 50, 255, cv2.THRESH_BINARY_INV )
    imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imginv)
    img = cv2.bitwise_or(img,mask)

    img[0:128, 0:922] = l2[0]

    cv2.imshow("Image", img)
    # cv2.imshow("canvas", mask)
    cv2.waitKey(1)
