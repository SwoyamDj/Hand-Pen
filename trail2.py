import cv2
import mediapipe as mp
import time
import os
import htm
import numpy as np


taskbar="close"
mode="free"
present = "active"
#setting icons
s = cv2.imread("D:\Python\haand_gestures\proj\images\selected.png")
i = cv2.imread("images/idle.png")
icon= cv2.imread("D:\Python\haand_gestures\proj\images\icon.png")

op=[
    icon,
[s, i, i, i, i, icon],
[i, s, i, i, i, icon],
[i, i, s, i, i, icon],
[i, i, i, s, i, icon],
[i, i, i, i, s, icon],
    [i, i, i, i, i, icon],
]

header=op[1]
index=1
#^^^^^^^^^^^^^^^^^



def seticons(frame, header):
    if len(header)==1:
        frame[0:200][0:200] = header[0]
    else:
         frame[1000:1200][0:200] = header[index][5]
         for i in range(5):
            frame[36:(i+1)*200-36][0:128] = header[index][i]



def gesture(li, li2):
    x = [li2[4][2], li2[3][2], li2[6][2], li2[10][2], li2[14][2], li2[18][2]]
    if li[1] == 1 and li[2] == 1:
        return "select"
    elif li[1] == 1:
        return "draw"
    elif x == sorted(x):
        return "thumbsup"
    else:
        return "free"

# mask = np.zeros((720,1280,3),np.uint8)
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

while True:
    _, frame = cap.read()
    # detect = htm.handDetector(detectionCon=0.6)
    # detect.findHands(frame,draw=False)
    # l3 = detect.findPosition(frame, draw=False)
    # l4 = detect.fingersUp()
    # if len(l3)!=0:
    #     xm, ym = l3[8][1:]
    # if len(l4)!=0:
    #     mode = gesture(l4,l3)
    #
    # #selection
    #
    #
    # if mode == "select":
    #     if taskbar=="open":
    #         if ym < 128:
    #             if 0 < xm < 200:
    #                 choice = "writer"
    #                 index=1
    #             elif xm < 370:
    #                 choice = "line"
    #                 index = 2
    #             elif 370 < xm < 555:
    #                 choice = "rectangle"
    #                 index = 3
    #             elif 555 < xm < 740:
    #                 choice = "circle"
    #                 index = 4
    #             elif 740< xm < 940:
    #                 choice = "eraser"
    #                 index = 5
    #             elif 1000 < xm < 1200:
    #                 taskbar="close"
    #                 '''set index no as somthing to remember prev state'''
    #     else:
    #         if ym < 128:
    #             if 1000 < xm < 1200:
    #                 taskbar="open"
    #                 header = op[index]
    #                 '''koi image ka list use set index no list to call back'''
    #
    # #updation of toolbar


    # if len(header)==1:
    frame[5:205, 1040:1240] = s
    # seticons(frame, header)
    cv2.imshow("canvas", frame)
    cv2.waitKey(1)