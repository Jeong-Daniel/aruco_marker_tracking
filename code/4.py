# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:55:16 2021
@author: dhjun
"""
#라이브러리, OpenCV,numpy,math사용
import cv2
import cv2.aruco as aruco
import numpy as np
from math import pi, sqrt, atan2, asin
#import matplotlib.pyplot as plt
#from scipy.spatial.transform import Rotation

#서보모터 각도 제어를 위한 모듈
import pigpio
from time import sleep
pie = pigpio.pi()
#sudo pigpiod
# 사용해려는 행렬이 유효한지 확인
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

#t벡터와 r벡터를 문자열 변환함수로 변환한다음 출력하기 위한 함수
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

def convert(angle):
    angle = round(angle,0)
    angle += 90
    if angle < 0:
        angle =0
    if angle > 180:
        angle = 180
    return 600 + angle*10

#오일러 각도에 대한 회전 행렬 계산
#오일러 각도에 대해서 x와 z를 교환함
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
    
    Rstr = [x,y,z]
    return Rstr

def rotationMatrixToEulerAngles_C(R) :
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

    x=round(x,5)
    y=round(y,5)
    z=round(z,5)
    
    Rstr = ['C_Pitch:'+str(x),'C_Yaw: '+str(y),'C_Roll: '+str(z)]
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

"""
def eulerAnglesToRotationMatrix(euler):
     R_x = np.array([[                1,                 0,                 0],
                     [                0,  np.cos(euler[0]), -np.sin(euler[0])],
                     [                0,  np.sin(euler[0]),  np.cos(euler[0])]])
     R_y = np.array([[ np.cos(euler[1]),                 0,  np.sin(euler[1])],
                     [ 0,                                1,                 0],
                     [-np.sin(euler[1]),                 0,  np.cos(euler[1])]])
     R_z = np.array([[ np.cos(euler[2]), -np.sin(euler[2]),                 0],
                     [ np.sin(euler[2]),  np.cos(euler[2]),                 0],
                     [                0,                 0,                 1]])
     R = np.dot(R_z, np.dot(R_y, R_x))
     return R
"""

#비디오불러오기, 640x480으로 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

#위에서부터 마커사이즈(단위m),왜곡계수,카메라포즈
marker_size=0.15
#distCoeffs=np.array([k1, k2, p1, p2, k3])
#rasberry pi camera
distCoeffs=np.array([-0.006462, 0.852629,-0.003371,-0.003302, 0])
K = np.array([[914.426678, 0, 640],
              [0, 914.426678, 360],
              [0, 0, 1]], dtype=np.float32)
"""
#서피스랩탑4
distCoeffs=np.array([0.015701, 0.190824, 0.001675, -0.003972, 0])
K = np.array([[623.798362, 0, 320],
              [0, 623.798362, 240],
              [0, 0, 1]], dtype=np.float32)
##레노버
distCoeffs=np.array([0.010161, -0.090434, 0.007061, 0.002154, 0])
K = np.array([[572.434936, 0, 320],
              [0, 572.434936, 240],
              [0, 0, 1]], dtype=np.float32)
"""
#출력에 사용할 폰트
font=cv2.FONT_HERSHEY_SIMPLEX
trans = []
angle = []

#17,18,27번의 서보모터를 종료함
pie.set_servo_pulsewidth(17, 0) 
pie.set_servo_pulsewidth(18, 0)
pie.set_servo_pulsewidth(27, 0)
sleep(0.1)

while True:
    ret, frame = cap.read()
    #검출률을 높이기 위해서 그레이스케일로 변환한 이미지 사용
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #마커의 코너와 id(마커번호)
    corners, ids, _ = aruco.detectMarkers(gray, dictionary)
    #주어진 파라메타를 통해서 회전벡터와 트랜잭션벡터
    rvecs, tvecs, __ = aruco.estimatePoseSingleMarkers(corners, marker_size, K, distCoeffs)
      
    #코너가 한개이상 나올때(마커가 감지될때)
    if len(corners) > 0:
        #마커 그리기
        aruco.drawDetectedMarkers(frame,corners,ids)
        #마커 축 그리기
        aruco.drawAxis(frame, K, distCoeffs, rvecs, tvecs, 0.1)
        #영상위에 글 출력
        cv2.putText(frame, vtos(tvecs), (0, 100), font, 1, (139, 0, 255))
        trans.append(g_v(tvecs))
        R = cv2.Rodrigues(rvecs)[0]
        R_T = R.T

        Rstr_A = rotationMatrixToEulerAngles(R)
        cv2.putText(frame, 'Pitch:'+str(Rstr_A[0]), (0, 150), font, 1, (0, 255, 0))
        cv2.putText(frame, 'Yaw: '+str(Rstr_A[1]), (0, 200), font, 1, (255, 0, 0))
        cv2.putText(frame, 'Roll: '+str(Rstr_A[2]), (0, 250), font, 1, (0, 0, 255))
        angle.append(graph(R))
        
        Rstr_C = rotationMatrixToEulerAngles_C(R_T)
        cv2.putText(frame, Rstr_C[0], (0, 300), font, 1, (0, 255, 0))
        cv2.putText(frame, Rstr_C[1], (0, 350), font, 1, (255, 0, 0))
        cv2.putText(frame, Rstr_C[2], (0, 400), font, 1, (0, 0, 255))
    
        #17 Pitch, 18 yaw, 27 roll
        pie.set_servo_pulsewidth(17, convert(Rstr_A[0]))
        pie.set_servo_pulsewidth(18, convert(Rstr_A[1]))
        pie.set_servo_pulsewidth(27, convert(Rstr_A[2]))
        sleep(0.1)

    #영상출력
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #서보모터 동작을 위한 텀주기
    
cap.release()
cv2.destroyAllWindows()

#plt.title("angle"); plt.plot(angle); plt.show()
#plt.title("trans"); plt.plot(trans); plt.show()