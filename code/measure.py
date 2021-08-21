# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 17:02:26 2021

@author: dhjun
"""

import cv2
import cv2.aruco as aruco
import numpy as np
import pandas as pd
from math import pi, sqrt, atan2, asin

def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

def vtos(rvecs):
    temp = np.round_(rvecs[0].reshape((3, 1)),5)
    temp*=100
    Rstr = 'X:'+str(temp[0])+'  Y:'+str(temp[1])+'  Z:'+str(temp[2])
    return Rstr

def g_v(rvecs):
    temp = np.round_(rvecs[0].reshape((3, 1)),5)
    temp.tolist()
    temp=[temp[0][0],temp[1][0],temp[2][0]]
    return temp

def rotationMatrixToEulerAngles(R) :
    assert(isRotationMatrix(R))
    sy = sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if  not singular :
        x = 180*atan2(R[2,1] , R[2,2])/pi
        y = 180*atan2(-R[2,0], sy)/pi
        z = 180*atan2(R[1,0], R[0,0])/pi
    else :
        x = 180*atan2(-R[1,2], R[1,1])/pi
        y = 180*atan2(-R[2,0], sy)/pi
        z = 0
    
    if x < 0:
        x+=180
    else:
        x-=180
        
    x=round(x,5)
    y=round(y,5)
    z=round(z,5)
    
    Rstr = ['Pitch:'+str(x),'Yaw: '+str(y),'Roll: '+str(z)]
    return Rstr

def graph(R):
    assert(isRotationMatrix(R))
    sy = sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if  not singular :
        x = 180*atan2(R[2,1] , R[2,2])/pi
        y = 180*atan2(-R[2,0], sy)/pi
        z = 180*atan2(R[1,0], R[0,0])/pi
    else :
        x = 180*atan2(-R[1,2], R[1,1])/pi
        y = 180*atan2(-R[2,0], sy)/pi
        z = 0
    if x < 0:
        x+=180
    else:
        x-=180
    return [x,y,z]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

marker_size=0.15
#distCoeffs=np.array([k1, k2, p1, p2, k3])
distCoeffs=np.array([-0.006462, 0.852629,-0.003371,-0.003302, 0])
K = np.array([[914.426678, 0, 640],
              [0, 914.426678, 360],
              [0, 0, 1]], dtype=np.float32)

font=cv2.FONT_HERSHEY_SIMPLEX
df_angle = pd.DataFrame(columns = ['pitch' , 'yaw', 'roll'])
df_trans = pd.DataFrame(columns = ['x' , 'y', 'z'])

import datetime
now = str(datetime.datetime.now().strftime("%d_%H-%M-%S"))

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, dictionary)
    rvecs, tvecs, __ = aruco.estimatePoseSingleMarkers(corners, marker_size, K, distCoeffs)
    
    if len(corners) > 0:
        aruco.drawDetectedMarkers(frame,corners,ids)
        aruco.drawAxis(frame, K, distCoeffs, rvecs, tvecs, 0.1)
        cv2.putText(frame, vtos(tvecs), (0, 100), font, 1, (139, 0, 255))
        df_trans.loc[len(df_trans)] = [g_v(tvecs)[0],g_v(tvecs)[1],g_v(tvecs)[2]]
        R = cv2.Rodrigues(rvecs)[0]

        Rstr_A = rotationMatrixToEulerAngles(R)
        cv2.putText(frame, Rstr_A[0], (0, 150), font, 1, (0, 255, 0))
        cv2.putText(frame, Rstr_A[1], (0, 200), font, 1, (255, 0, 0))
        cv2.putText(frame, Rstr_A[2], (0, 250), font, 1, (0, 0, 255))
        df_angle.loc[len(df_angle)] = [graph(R)[0],graph(R)[1],graph(R)[2]]
        
    #영상출력
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

df_trans.to_csv(now + "_trans.csv", mode='w')
df_angle.to_csv(now+ "_angle.csv", mode='w')
cap.release()
cv2.destroyAllWindows()

#plt.title("angle"); plt.plot(angle); plt.show()
#plt.title("trans"); plt.plot(trans); plt.show()