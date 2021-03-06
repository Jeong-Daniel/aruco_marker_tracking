# 부산대학교 Aerospace Capstone Desing
# 항공우주종합설계(졸업논문)  
* 참여자 : 정대현(조장), 박유경(조원) | 지도교수 : 이대우 교수
---
### 주제 : 영상후처리를 통한 ArucoMarker 인식도개선  
* 본 프로젝트의 설계목표는 OpenCV(Open Source Computer Vision)와 ArucoMarker를 이용한 위치 및 자세 추정과 모델을 이용한 검증이다. 4차 산업 혁명과 함께 컴퓨터 비전의 기술이 빠르게 발전을 하고 있다. 많은 센서 대신 간단한 카메라만으로 자세 추정이라는 목표를 달성하고자 한다. 영상인식에 문제는 카메라의 기구적인 왜곡과 영상의 노이즈다. 문제를 해 결하기 위해 카메라 캘리브레이션과 임계 값 처리 등 영상 후처리 기법을 통해 노이즈를 제거하며 자세 추정의 안정성을 높이고자 한다. RGB색상 공간의 원본을 사용했을 때보다 값의 편차가 20% 내외로 감소하였으며 영상의 후처리에 따라 검출의 안정성을 개선할 수 있다.
### 결론
* 일반적으로 물체 검출에 있어서 수학적인 객체 검출 알고리즘 자체에 집중하거나 추가적인 장치 또는 식별마커 이외에 대상에 다른 표식 등을 추가하는 방법이 대부분이었다. 본 프로젝트에서는 식별마커 검출에 있어 다른 외적인 요소 대신 오로지 영상 후처리하는 방법으로 개선하는 쪽으로 접근하여 목표에 부합하는 결과를 얻을 수 있었다. 
---
#### 사용장비 & 라이브러리
* 라즈베리파이4
* 라즈베리파이 카메라모듈 V2, 8MP (RPI 8MP CAMERA BOARD)
* 파이썬(3.7)
* OpenCV (4.5.1)
* pigpio (서보모터 제어 라이브러리)