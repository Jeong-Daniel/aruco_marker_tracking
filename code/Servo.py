import pigpio
#sudo pigpiod
from time import sleep

 

pi = pigpio.pi() #먼저 사용할 pigpio.pi를 매칭해줍니다.

while True:
    pi.set_servo_pulsewidth(17, 0) #18번 채널에연결된 서보모터를 꺼줍니다.
    pi.set_servo_pulsewidth(18, 0)
    pi.set_servo_pulsewidth(27, 0)
    sleep(1)
    pi.set_servo_pulsewidth(17, 1500) # 가운데로 이동 90도
    pi.set_servo_pulsewidth(18, 1500)
    pi.set_servo_pulsewidth(27, 1500)
    sleep(1)