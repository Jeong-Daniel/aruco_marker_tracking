# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 21:43:21 2021

@author: dhjun
"""

import datetime
import cv2
#import os

#path = 'C:\test'
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv2.CAP_PROP_FPS, 60)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
record = False
while True:
    ret, frame = capture.read()
    cv2.imshow("VideoFrame", frame)

    now = str(datetime.datetime.now().strftime("%d_%H-%M-%S"))
    key = cv2.waitKey(33)

    if key == 27:
        break
    elif key == 26:
        print("캡쳐")
        #cv2.imwrite(os.path.join(path , f'{now}.jpg', frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0]))
        cv2.imwrite("./"+now+".png", frame)
    elif key == 24:
        print("녹화 시작")
        record = True
        video = cv2.VideoWriter("D:/" + str(now) + ".avi", fourcc, 20.0, (frame.shape[1], frame.shape[0]))
    elif key == 3:
        print("녹화 중지")
        record = False
        video.release()
        
    if record == True:
        print("녹화 중..")
        video.write(frame)

capture.release()
cv2.destroyAllWindows()
