# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 22:09:54 2021

@author: dhjun
"""

#!/opt/local/bin/python
# -*- coding: utf-8 -*-
import picamera                   # 라즈베리파이 카메라용 라이브러리 로드
import time                       # sleep을 사용하기 위한 라이브러리
import datetime
path = "C:\\Users\\dhjun\\Documents\\"
now = str(datetime.datetime.now().strftime("%d_%H-%M-%S"))
cam = picamera.PiCamera()         # 라즈베리파이 카메라 열기
cam.start_preview()               # 카메라 Preview 시작
time.sleep(5)                    # 10초간 대기
cam.stop_preview()                # 카메라 Preview 정지
cam.capture(paht+now+'png') # 카메라 캡쳐 (image.jpg로 저장)

# -*- coding: utf-8 -*-
"""
import cv2
import datetime

path = "C:\\Users\\dhjun\\Documents\\"
CAM_ID = 0
def capture(camid = CAM_ID):
    cam = cv2.VideoCapture(camid)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    if cam.isOpened() == False:
        print ('cant open the cam (%d)' % camid)
        return None

    ret, frame = cam.read()
    if frame is None:
        print ('frame is not exist')
        return None
    now = str(datetime.datetime.now().strftime("%d_%H-%M-%S"))
    # png로 압축 없이 영상 저장
    cv2.imwrite(path+now+".png",frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cam.release()
    
if __name__ == '__main__':
    capture()
"""
